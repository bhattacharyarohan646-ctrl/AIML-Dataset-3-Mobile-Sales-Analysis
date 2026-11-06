
# Q1: Mobile Brand with the Highest Number of Models

import pandas as pd

df = pd.read_csv("MobSales.csv")

brand_count = df.groupby("Brands")["Models"].nunique().reset_index()

brand_count.columns = ["Brand", "Total_Models"]

brand_count = brand_count.sort_values(
    by="Total_Models",
    ascending=False
)

print("\nQ1: Mobile Brands by Number of Models")
print(brand_count.to_string(index=False))

brand_count.to_csv("Q1_Brand_Model_Count.csv", index=False)

print("\nResult saved successfully!")




# Q2: Top 10 Mobile Models Based on Selling Price

top_10_price = df.sort_values(
    by="Selling Price",
    ascending=False
).head(10)

result = top_10_price[["Brands", "Models", "Selling Price"]]

print("\nQ2: Top 10 Mobile Models by Selling Price")
print(result.to_string(index=False))

result.to_csv("Q2_Top_10_Expensive_Mobiles.csv", index=False)

print("\nResult saved successfully!")



# Q3: Average Selling Price for Each Mobile Brand

average_price = df.groupby("Brands")["Selling Price"].mean().reset_index()

average_price.columns = ["Brand", "Average_Selling_Price"]

average_price["Average_Selling_Price"] = average_price[
    "Average_Selling_Price"
].round(2)

average_price = average_price.sort_values(
    by="Average_Selling_Price",
    ascending=False
)

print("\nQ3: Average Selling Price by Brand")
print(average_price.to_string(index=False))

average_price.to_csv("Q3_Average_Selling_Price_By_Brand.csv", index=False)

print("\nResult saved successfully!")



# Q4: Mobile Brand with the Highest Average Discount

average_discount = df.groupby("Brands")["Discount"].mean().reset_index()

average_discount.columns = ["Brand", "Average_Discount"]

average_discount["Average_Discount"] = average_discount[
    "Average_Discount"
].round(2)

average_discount = average_discount.sort_values(
    by="Average_Discount",
    ascending=False
)

print("\nQ4: Average Discount by Brand")
print(average_discount.to_string(index=False))

print("\nBrand Offering the Highest Average Discount:")
print(average_discount.head(1).to_string(index=False))

average_discount.to_csv("Q4_Average_Discount_By_Brand.csv", index=False)

print("\nResult saved successfully!")






# Q5: Average Customer Rating and Selling Price by Brand

brand_analysis = df.groupby("Brands").agg(
    Average_Rating=("Rating", "mean"),
    Average_Selling_Price=("Selling Price", "mean")
).reset_index()

brand_analysis["Average_Rating"] = brand_analysis[
    "Average_Rating"
].round(2)

brand_analysis["Average_Selling_Price"] = brand_analysis[
    "Average_Selling_Price"
].round(2)

brand_analysis = brand_analysis.sort_values(
    by="Average_Rating",
    ascending=False
)

print("\nQ5: Brand Rating and Average Selling Price")
print(brand_analysis.to_string(index=False))

print("\nTop Rated Mobile Brand:")
print(brand_analysis.head(1).to_string(index=False))

brand_analysis.to_csv("Q5_Brand_Rating_and_Price.csv", index=False)

print("\nResult saved successfully!")



# Q6: Effect of Storage Capacity on Average Selling Price

storage_analysis = df.groupby("Storage").agg(
    Total_Mobiles=("Models", "count"),
    Average_Selling_Price=("Selling Price", "mean")
).reset_index()

storage_analysis["Average_Selling_Price"] = storage_analysis[
    "Average_Selling_Price"
].round(2)

storage_analysis = storage_analysis.sort_values(
    by="Average_Selling_Price",
    ascending=False
)

print("\nQ6: Storage Capacity vs Average Selling Price")
print(storage_analysis.to_string(index=False))

storage_analysis.to_csv("Q6_Storage_vs_Selling_Price.csv", index=False)

print("\nResult saved successfully!")




# Q7: Mobile Models with the Highest Discount Amount

discount_analysis = df[
    ["Brands", "Models", "Original Price", "Selling Price", "Discount"]
].copy()

# Calculate discount amount
discount_analysis["Discount_Amount"] = (
    discount_analysis["Original Price"] -
    discount_analysis["Selling Price"]
)

# Calculate discount percentage
discount_analysis["Discount_Percentage"] = (
    discount_analysis["Discount_Amount"] /
    discount_analysis["Original Price"].replace(0, pd.NA)
) * 100

discount_analysis["Discount_Percentage"] = (
    discount_analysis["Discount_Percentage"].round(2)
)

discount_analysis = discount_analysis.sort_values(
    by="Discount_Amount",
    ascending=False
).head(10)

print("\nQ7: Top 10 Mobile Models with Highest Discount")
print(discount_analysis.to_string(index=False))

discount_analysis.to_csv("Q7_Top_10_Highest_Discount.csv", index=False)

print("\nResult saved successfully!")


# Q8: Best Memory and Storage Combination

memory_storage_analysis = df.groupby(
    ["Memory", "Storage"]
).agg(
    Total_Mobiles=("Models", "count"),
    Average_Selling_Price=("Selling Price", "mean"),
    Average_Rating=("Rating", "mean")
).reset_index()

memory_storage_analysis["Average_Selling_Price"] = (
    memory_storage_analysis["Average_Selling_Price"].round(2)
)

memory_storage_analysis["Average_Rating"] = (
    memory_storage_analysis["Average_Rating"].round(2)
)

# Give priority to higher ratings and lower prices
memory_storage_analysis = memory_storage_analysis.sort_values(
    by=["Average_Rating", "Average_Selling_Price"],
    ascending=[False, True]
)

print("\nQ8: Memory and Storage Combination Analysis")
print(memory_storage_analysis.to_string(index=False))

memory_storage_analysis.to_csv(
    "Q8_Memory_Storage_Analysis.csv",
    index=False
)

print("\nResult saved successfully!")



# Q9: Top 10 Mobile Models by Value for Money Score

value_data = df[
    ["Brands", "Models", "Selling Price", "Original Price",
     "Discount", "Storage", "Memory", "Rating"]
].copy()

# Convert Memory and Storage into numeric GB values
def convert_to_gb(value):
    value = str(value).upper().replace(" ", "")
    try:
        if "TB" in value:
            return float(value.replace("TB", "")) * 1024
        elif "GB" in value:
            return float(value.replace("GB", ""))
        else:
            return float(value)
    except:
        return None

value_data["Storage_GB"] = value_data["Storage"].apply(convert_to_gb)
value_data["Memory_GB"] = value_data["Memory"].apply(convert_to_gb)

# Calculate discount percentage
value_data["Discount_Percentage"] = (
    (value_data["Original Price"] - value_data["Selling Price"]) /
    value_data["Original Price"].replace(0, pd.NA)
) * 100

# Convert relevant columns to numeric
score_columns = [
    "Selling Price", "Discount_Percentage",
    "Storage_GB", "Memory_GB", "Rating"
]

for col in score_columns:
    value_data[col] = pd.to_numeric(value_data[col], errors="coerce")

value_data = value_data.dropna(subset=score_columns)

# Min-Max Normalization
def normalize(series):
    if series.max() == series.min():
        return pd.Series(0, index=series.index)
    return (series - series.min()) / (series.max() - series.min())

value_data["Rating_Score"] = normalize(value_data["Rating"])
value_data["Discount_Score"] = normalize(value_data["Discount_Percentage"])
value_data["Storage_Score"] = normalize(value_data["Storage_GB"])
value_data["Memory_Score"] = normalize(value_data["Memory_GB"])

# Lower selling price gets a higher score
value_data["Price_Score"] = 1 - normalize(value_data["Selling Price"])

# Calculate Value for Money Score
value_data["Value_Score"] = (
    0.30 * value_data["Rating_Score"] +
    0.20 * value_data["Discount_Score"] +
    0.20 * value_data["Storage_Score"] +
    0.15 * value_data["Memory_Score"] +
    0.15 * value_data["Price_Score"]
) * 100

top_10_value = value_data.sort_values(
    by="Value_Score",
    ascending=False
).head(10)

result = top_10_value[
    ["Brands", "Models", "Selling Price", "Discount_Percentage",
     "Storage", "Memory", "Rating", "Value_Score"]
]

print("\nQ9: Top 10 Mobiles by Value for Money Score")
print(result.round(2).to_string(index=False))

result.to_csv("Q9_Top_10_Value_for_Money.csv", index=False)

print("\nResult saved successfully!")

# Q10: Good Product Analysis

import matplotlib.pyplot as plt
import seaborn as sns

good_data = df[
    ["Selling Price", "Original Price", "Discount",
     "Rating", "Memory", "Storage", "Good Product"]
].copy()

# Convert Memory and Storage into numeric GB values
def convert_to_gb(value):
    value = str(value).upper().replace(" ", "")
    try:
        if "TB" in value:
            return float(value.replace("TB", "")) * 1024
        elif "GB" in value:
            return float(value.replace("GB", ""))
        else:
            return float(value)
    except:
        return None

good_data["Memory_GB"] = good_data["Memory"].apply(convert_to_gb)
good_data["Storage_GB"] = good_data["Storage"].apply(convert_to_gb)

# Convert numeric columns
numeric_columns = [
    "Selling Price", "Discount", "Rating",
    "Memory_GB", "Storage_GB"
]

for col in numeric_columns:
    good_data[col] = pd.to_numeric(good_data[col], errors="coerce")

# Convert Good Product into numeric format
good_data["Good_Product_Flag"] = (
    good_data["Good Product"]
    .astype(str).str.strip().str.lower()
    .map({"yes": 1, "no": 0, "true": 1, "false": 0, "1": 1, "0": 0})
)

good_data = good_data.dropna(
    subset=numeric_columns + ["Good_Product_Flag"]
)

# Compare average values
comparison = good_data.groupby("Good_Product_Flag")[
    numeric_columns
].mean().round(2)

comparison.index = comparison.index.map({
    1: "Good Product",
    0: "Not Good Product"
})

print("\nQ10: Good Product vs Not Good Product")
print(comparison.to_string())

# Correlation with Good Product classification
correlation = good_data[
    numeric_columns + ["Good_Product_Flag"]
].corr()["Good_Product_Flag"].drop("Good_Product_Flag")

correlation = correlation.sort_values(
    key=abs,
    ascending=False
).round(3)

print("\nFactors Most Strongly Related to Good Product:")
print(correlation.to_string())

# Save results
comparison.to_csv("Q10_Good_Product_Comparison.csv")
correlation.to_csv("Q10_Good_Product_Correlation.csv")

# Create correlation chart
plt.figure(figsize=(9, 5))
sns.barplot(x=correlation.values, y=correlation.index)
plt.title("Factors Related to Good Product Classification")
plt.xlabel("Correlation with Good Product")
plt.ylabel("Factors")
plt.tight_layout()
plt.savefig("Q10_Good_Product_Correlation.png")
plt.show()

print("\nAll Q10 results saved successfully!")

