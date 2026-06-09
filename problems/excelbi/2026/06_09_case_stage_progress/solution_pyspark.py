from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from utils import show

spark = SparkSession.builder.appName("Case Stage Progress").getOrCreate()

data_file = str(Path(__file__).parent / "data" / "cases.csv")

df = spark.read.option("header", True).option("inferSchema", True).csv(data_file)

stage_summary = df.groupBy("CaseID").agg(
    F.coalesce(F.max(F.when(F.col("Cleared"), F.col("StageNo"))), F.lit(0)).alias(
        "CurrentStageNo"
    ),
    F.coalesce(
        F.min(F.when(~F.col("Cleared"), F.col("StageNo"))), F.max("StageNo") + F.lit(1)
    ).alias("FirstUnclearedStageNo"),
    F.round(
        F.avg(F.when(F.col("Cleared"), F.lit(1.0)).otherwise(F.lit(0.0))) * 100, 0
    ).alias("ProgressPct"),
)

current_stage = (
    stage_summary.alias("s")
    .join(
        df.alias("c"),
        (
            (F.col("s.CaseID") == F.col("c.CaseID"))
            & (F.col("s.CurrentStageNo") == F.col("c.StageNo"))
        ),
        "left",
    )
    .select(
        F.col("s.CaseID"),
        F.coalesce(F.col("c.StageName"), F.lit("Not Started")).alias("CurrentStage"),
    )
)

next_stage_candidates = df.alias("c").join(
    stage_summary.alias("s"),
    (
        (F.col("c.CaseID") == F.col("s.CaseID"))
        & (~F.col("c.Cleared"))
        & (F.col("c.StageNo") > F.col("s.CurrentStageNo"))
    ),
    "inner",
)

next_stage_window = Window.partitionBy("c.CaseID").orderBy("c.StageNo")

next_stage_candidates = next_stage_candidates.withColumn(
    "rn", F.row_number().over(next_stage_window)
)

next_stage = next_stage_candidates.filter(F.col("rn") == 1).select(
    F.col("c.CaseID").alias("CaseID"), F.col("c.StageName").alias("NextStage")
)

result = (
    stage_summary.alias("s")
    .join(current_stage.alias("cs"), "CaseID", "left")
    .join(next_stage.alias("ns"), "CaseID", "left")
    .select(
        F.col("CaseID"),
        F.col("CurrentStage"),
        F.coalesce(F.col("NextStage"), F.lit("Completed")).alias("NextStage"),
        F.when(F.col("ProgressPct") == 0, F.lit("Not Started"))
        .when(F.col("ProgressPct") == 100, F.lit("Completed"))
        .otherwise(F.lit("In Progress"))
        .alias("Status"),
        F.when(F.col("CurrentStageNo") > F.col("FirstUnclearedStageNo"), F.lit("Yes"))
        .otherwise(F.lit("No"))
        .alias("ProcessIssue"),
        F.concat(F.col("ProgressPct").cast("int"), F.lit("%")).alias("ProgressPct"),
    )
    .orderBy("CaseID")
)

show(result.toPandas(), "Case Summary")

spark.stop()
