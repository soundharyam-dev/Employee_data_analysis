import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)
import os


# Load the CSV dataset
df = pd.read_csv("employees.csv")

# 1. Display the first five rows
print("First five rows:")
print(df.head())

# 2. Display the last five rows
print("\nLast five rows:")
print(df.tail())

# 3. Find the total number of rows and columns
print("\nNumber of rows and columns:")
print(df.shape)

print("Total rows:", df.shape[0])
print("Total columns:", df.shape[1])

# 4. Display all column names
print("\nColumn names:")
print(df.columns.tolist())

# 5. Check each column's data type
print("\nColumn data types:")
print(df.dtypes)

# 6. Count missing values in every column
print("\nMissing values in each column:")
print(df.isnull().sum())

# 7. Check the number of duplicate rows
print("\nNumber of duplicate rows:")
print(df.duplicated().sum())




# Step 2: Display missing values before cleaning
print("Missing values BEFORE cleaning:")
print(df.isnull().sum())

# Step 3: Remove the completely empty column
df = df.dropna(axis=1, how="all")

# Step 4: Fix data types
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["monthly_income"] = pd.to_numeric(
    df["monthly_income"].astype(str).str.replace(",", "", regex=False),
    errors="coerce"
)
df["joining_date"] = pd.to_datetime(
    df["joining_date"], errors="coerce"
)

# Step 5: Fill missing numerical values with the median
df["age"] = df["age"].fillna(df["age"].median())
df["monthly_income"] = df["monthly_income"].fillna(
    df["monthly_income"].median()
)

# Step 6: Fill missing categorical values with the mode
for col in ["name", "department", "city"]:
    df[col] = df[col].fillna(df[col].mode()[0])

# Step 7: Fill missing joining dates with the median date
median_date = df["joining_date"].dropna().median()
df["joining_date"] = df["joining_date"].fillna(median_date)

# Step 8: Display missing values after cleaning
print("\nMissing values AFTER cleaning:")
print(df.isnull().sum())

print("\nTotal missing values after cleaning:")
print(df.isnull().sum().sum())

#check data types
print("\n check data types:")
print(df.dtypes)


#check duplicated rows
print("\n check duplicated rows:")
print(df.duplicated().sum())


#remove duplicates
df = df.drop_duplicates()



# Step 9: Save the cleaned dataset
df.to_csv("employee_records_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully!")
print("\nMissing values:")
print(df.isnull().sum())

# Step 7: Display the data
print("\nCleaned dataset:")
print(df.head())


# Statistical summary
print("\nStatistical Summary:")
print(df.describe())

# Individual statistics
print("\nAverage age:", df["age"].mean())
print("Median age:", df["age"].median())
print("Minimum age:", df["age"].min())
print("Maximum age:", df["age"].max())

print("\nAverage monthly income:", df["monthly_income"].mean())
print("Median monthly income:", df["monthly_income"].median())
print("Minimum monthly income:", df["monthly_income"].min())
print("Maximum monthly income:", df["monthly_income"].max())

#no of employees in each department
print("\nEmployees by Department:")
print(df["department"].value_counts())

#average income by department
print("\nAverage Income by Department:")
print(
    df.groupby("department")["monthly_income"]
    .mean()
    .sort_values(ascending=False)
)

#employees by city
print("\nEmployees by City:")
print(df["city"].value_counts())

#employee age group
print("\nEmployee Age Groups:")

age_groups = pd.cut(
    df["age"],
    bins=[0, 25, 35, 45, 55, 100],
    labels=["18-25", "26-35", "36-45", "46-55", "56+"]
)

print(age_groups.value_counts().sort_index())


#employee joining by year
print("\nEmployees Joining by Year:")

print(
    df["joining_date"]
    .dt.year
    .value_counts()
    .sort_index()
)

#employee age distribution

plt.figure(figsize=(8, 5))
plt.hist(df["age"], bins=10, edgecolor="black")
plt.title("Employee Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Employees")
plt.tight_layout()
plt.savefig("charts/chart1_age_distribution.png", dpi=300)
plt.show()


# CHART 2: Employees by Department
plt.figure(figsize=(8, 5))
df["department"].value_counts().plot(kind="bar")
plt.title("Employees by Department")
plt.xlabel("Department")
plt.ylabel("Number of Employees")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/chart2_department_count.png", dpi=300)
plt.close()


# CHART 3: Average Monthly Income by Department
plt.figure(figsize=(8, 5))
sns.barplot(
    data=df,
    x="department",
    y="monthly_income",
    errorbar=None
)
plt.title("Average Monthly Income by Department")
plt.xlabel("Department")
plt.ylabel("Average Monthly Income")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/chart3_department_income.png", dpi=300)
plt.close()


# CHART 4: Monthly Income Distribution
plt.figure(figsize=(8, 5))
sns.boxplot(x=df["monthly_income"].dropna())
plt.title("Monthly Income Distribution")
plt.xlabel("Monthly Income")
plt.tight_layout()
plt.savefig("charts/chart4_income_boxplot.png", dpi=300)
plt.close()


# CHART 5: Age vs Monthly Income
plot_df = df.dropna(
    subset=["age", "monthly_income", "department"]
)

plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=plot_df,
    x="age",
    y="monthly_income",
    hue="department"
)
plt.title("Age vs Monthly Income")
plt.xlabel("Age")
plt.ylabel("Monthly Income")
plt.tight_layout()
plt.savefig("charts/chart5_age_income.png", dpi=300)
plt.close()

print("All 5 charts saved successfully in the charts folder!")



# STEP 2: Prepare report
output_file = "output/Employee_Analysis_Report.pdf"

doc = SimpleDocTemplate(
    output_file,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)

styles = getSampleStyleSheet()
story = []

# STEP 3: Report title
story.append(Paragraph(
    "Employee Data Analysis Report",
    styles["Title"]
))
story.append(Spacer(1, 12))

story.append(Paragraph(
    "This report summarizes the employee dataset after "
    "data cleaning, statistical analysis, and visualization.",
    styles["BodyText"]
))
story.append(Spacer(1, 15))

# STEP 4: Dataset overview
story.append(Paragraph("1. Dataset Overview", styles["Heading1"]))

overview = [
    ["Metric", "Result"],
    ["Total employees (rows)", str(len(df))],
    ["Total columns", str(len(df.columns))],
    ["Duplicate rows", str(df.duplicated().sum())],
    ["Missing values", str(df.isnull().sum().sum())]
]

table = Table(overview, colWidths=[220, 200])
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("PADDING", (0, 0), (-1, -1), 7),
]))
story.append(table)
story.append(Spacer(1, 15))

# STEP 5: Calculate statistics
story.append(Paragraph("2. Statistical Summary", styles["Heading1"]))

age_mean = df["age"].mean()
age_median = df["age"].median()
income_mean = df["monthly_income"].mean()
income_median = df["monthly_income"].median()

statistics = [
    ["Statistic", "Age", "Monthly Income"],
    [
        "Average",
        f"{age_mean:.2f}" if pd.notna(age_mean) else "N/A",
        f"{income_mean:,.2f}" if pd.notna(income_mean) else "N/A"
    ],
    [
        "Median",
        f"{age_median:.2f}" if pd.notna(age_median) else "N/A",
        f"{income_median:,.2f}" if pd.notna(income_median) else "N/A"
    ],
    [
        "Minimum",
        f"{df['age'].min():.2f}" if df["age"].notna().any() else "N/A",
        f"{df['monthly_income'].min():,.2f}"
        if df["monthly_income"].notna().any() else "N/A"
    ],
    [
        "Maximum",
        f"{df['age'].max():.2f}" if df["age"].notna().any() else "N/A",
        f"{df['monthly_income'].max():,.2f}"
        if df["monthly_income"].notna().any() else "N/A"
    ]
]

table = Table(statistics, colWidths=[130, 130, 160])
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("PADDING", (0, 0), (-1, -1), 6),
]))
story.append(table)
story.append(Spacer(1, 15))

# STEP 6: Find patterns
story.append(Paragraph("3. Key Findings and Patterns", styles["Heading1"]))

findings = []

if df["department"].notna().any():
    dept_counts = df["department"].value_counts()
    findings.append(
        f"The department with the most employees is "
        f"{dept_counts.index[0]}, with {dept_counts.iloc[0]} employees."
    )

if df["city"].notna().any():
    city_counts = df["city"].value_counts()
    findings.append(
        f"The city with the most employees is "
        f"{city_counts.index[0]}, with {city_counts.iloc[0]} employees."
    )

dept_income = df.groupby("department")["monthly_income"].mean().dropna()

if not dept_income.empty:
    findings.append(
        f"{dept_income.idxmax()} has the highest average monthly income "
        f"({dept_income.max():,.2f})."
    )

correlation = df["age"].corr(df["monthly_income"])

if pd.notna(correlation):
    findings.append(
        f"The correlation between age and monthly income is "
        f"{correlation:.2f}. A positive value indicates an upward "
        f"linear relationship, while a negative value indicates a "
        f"downward linear relationship."
    )

if pd.notna(age_mean):
    findings.append(f"The average employee age is {age_mean:.1f} years.")

if pd.notna(income_mean):
    findings.append(
        f"The average monthly income is {income_mean:,.2f}."
    )

for finding in findings:
    story.append(Paragraph("• " + finding, styles["BodyText"]))
    story.append(Spacer(1, 6))

# STEP 7: Add the five visualizations
story.append(PageBreak())
story.append(Paragraph("4. Data Visualizations", styles["Heading1"]))

chart_files = [
    ("charts/chart1_age_distribution.png", "Chart 1: Employee Age Distribution"),
    ("charts/chart2_department_count.png", "Chart 2: Employees by Department"),
    ("charts/chart3_department_income.png", "Chart 3: Average Income by Department"),
    ("charts/chart4_income_boxplot.png", "Chart 4: Monthly Income Distribution"),
    ("charts/chart5_age_income.png", "Chart 5: Age vs Monthly Income")
]

for chart_path, chart_title in chart_files:
    if os.path.exists(chart_path):
        story.append(Paragraph(chart_title, styles["Heading2"]))
        img = Image(chart_path, width=6 * inch, height=3.3 * inch)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Spacer(1, 12))
    else:
        story.append(Paragraph(
            f"Chart not found: {chart_path}",
            styles["BodyText"]
        ))

# STEP 8: Conclusion
story.append(Paragraph("5. Conclusion", styles["Heading1"]))

story.append(Paragraph(
    "The employee dataset was cleaned and analyzed using Python, "
    "Pandas, Matplotlib, and Seaborn. Statistical measures were "
    "calculated, employee patterns were investigated, and five "
    "visualizations were prepared. These results help summarize "
    "employee demographics, income distribution, and differences "
    "between departments and cities.",
    styles["BodyText"]
))

# STEP 9: Export PDF
doc.build(story)

print("Report created successfully!")
print("Saved as:", os.path.abspath(output_file))



