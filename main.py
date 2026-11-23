import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Create folder for generated graphs
OUTPUT_DIR = Path("visualizations")
OUTPUT_DIR.mkdir(exist_ok=True)


# Load the student performance dataset
df = pd.read_csv("data/student-mat.csv", sep=";")

# Display the first 5 records
print("\n===== FIRST 5 RECORDS =====")
print(df.head())

# Display dataset dimensions
print("\n===== DATASET SIZE =====")
print("Total students:", df.shape[0])
print("Total features:", df.shape[1])

# Display column names
print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())

# Display data types and missing values
print("\n===== DATASET INFORMATION =====")
df.info()

# Display summary statistics
print("\n===== STATISTICAL SUMMARY =====")
print(df.describe())

# Check missing values
print("\n===== MISSING VALUES =====")
print(df.isnull().sum())


# ===== STUDENT PERFORMANCE ANALYSIS =====

print("\n===== FINAL GRADE ANALYSIS =====")

# Calculate basic statistics
average_grade = df["G3"].mean()
highest_grade = df["G3"].max()
lowest_grade = df["G3"].min()

print("Average final grade:", round(average_grade, 2))
print("Highest final grade:", highest_grade)
print("Lowest final grade:", lowest_grade)

# Classify students as Pass or Fail
df["result"] = df["G3"].apply(
    lambda grade: "Pass" if grade >= 10 else "Fail"
)

# Count students in each category
print("\n===== PASS / FAIL COUNT =====")
print(df["result"].value_counts())

# Calculate percentages
print("\n===== PASS / FAIL PERCENTAGE =====")
print(df["result"].value_counts(normalize=True) * 100)


# Create a histogram
plt.figure(figsize=(10, 6))


sns.histplot(
    data=df,
    x="G3",
    discrete=True,
    color="steelblue"
)

plt.xticks(range(0, 21))


plt.title("Distribution of Final Mathematics Grades")
plt.xlabel("Final Grade (0–20)")
plt.ylabel("Number of Students")

plt.tight_layout()
plt.savefig("visualizations/grade_distribution.png", dpi=300, bbox_inches="tight")
plt.close()


# ===== STUDY TIME ANALYSIS =====

print("\n===== STUDY TIME VS FINAL GRADE =====")

# Calculate average final grade for each study-time group
study_analysis = df.groupby("studytime")["G3"].mean()

print(study_analysis)

# Visualize the relationship
plt.figure(figsize=(9, 5))

sns.barplot(
    data=df,
    x="studytime",
    y="G3",
    estimator="mean",
    errorbar=None,
    color="steelblue"
)

plt.title("Average Final Grade by Weekly Study Time")
plt.xlabel("Weekly Study Time Category")
plt.ylabel("Average Final Grade")

plt.tight_layout()
plt.savefig("visualizations/study_time.png", dpi=300, bbox_inches="tight")
plt.close()


# ===== CORRELATION ANALYSIS =====

print("\n===== CORRELATION ANALYSIS =====")

# Select variables for analysis
features = [
    "studytime",
    "absences",
    "failures",
    "G1",
    "G2",
    "G3"
]

# Calculate Pearson correlation
correlation_matrix = df[features].corr()

print(correlation_matrix.round(2))

# Create correlation heatmap
plt.figure(figsize=(9, 6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    vmin=-1,
    vmax=1
)

plt.title("Correlation Between Student Performance Factors")

plt.tight_layout()
plt.savefig("visualizations/correlation_heatmap.png", dpi=300, bbox_inches="tight")
plt.close()


# ===== PREVIOUS FAILURES ANALYSIS =====

print("\n===== PREVIOUS FAILURES VS FINAL GRADE =====")

# Calculate average grade and number of students
failure_analysis = df.groupby("failures")["G3"].agg(
    average_grade="mean",
    student_count="count"
)

print(failure_analysis.round(2))

# Create boxplot
plt.figure(figsize=(9, 5))

sns.boxplot(
    data=df,
    x="failures",
    y="G3",
    color="steelblue"
)

plt.title("Final Mathematics Grades by Previous Failures")
plt.xlabel("Number of Previous Class Failures")
plt.ylabel("Final Grade (0–20)")

plt.tight_layout()
plt.savefig("visualizations/previous_failures.png", dpi=300, bbox_inches="tight")
plt.close()

# ===== PASS RATE BY PREVIOUS FAILURES =====

print("\n===== PASS RATE BY PREVIOUS FAILURES =====")

# Create a boolean column for passing
df["passed"] = df["G3"] >= 10

# Calculate group statistics
pass_analysis = df.groupby("failures").agg(
    total_students=("passed", "count"),
    passed_students=("passed", "sum"),
    pass_rate=("passed", "mean")
)

# Convert pass rate to percentage
pass_analysis["pass_rate"] *= 100

print(pass_analysis.round(2))

# Visualize pass rates
plt.figure(figsize=(9, 5))

sns.barplot(
    data=pass_analysis.reset_index(),
    x="failures",
    y="pass_rate",
    color="steelblue"
)

plt.title("Student Pass Rate by Previous Class Failures")
plt.xlabel("Number of Previous Class Failures")
plt.ylabel("Pass Rate (%)")
plt.ylim(0, 100)


plt.tight_layout()
plt.savefig("visualizations/pass_rate.png", dpi=300, bbox_inches="tight")
plt.close()


