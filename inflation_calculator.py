
# ============================================================
# CANADIAN INFLATION CALCULATOR
# Uses monthly CPI data from the Bank of Canada
# ============================================================

# 1. IMPORT LIBRARIES

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path


# 2. LOAD AND PREPARE CPI DATA

def load_data():

    file_path = Path("data/inflation_data.csv")

    if not file_path.exists():
        raise FileNotFoundError(
            "CPI data file not found. Check the data folder."
        )

    df = pd.read_csv(file_path, skiprows=8)

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    # Identify the date column
    date_column = next(
        (col for col in df.columns
         if col.lower() in ["date", "observation_date"]),
        df.columns[0]
    )

    # Identify the CPI column
    if "STATIC_INFLATIONCALC" in df.columns:
        cpi_column = "STATIC_INFLATIONCALC"
    else:
        # Use the remaining column if the standard name differs
        remaining_columns = [
            col for col in df.columns if col != date_column
        ]

        if not remaining_columns:
            raise ValueError("Could not identify the CPI column.")

        cpi_column = remaining_columns[0]

    # Rename columns
    df = df.rename(columns={
        date_column: "Date",
        cpi_column: "CPI"
    })

    # Convert date and CPI columns
    df["Date"] = pd.to_datetime(
        df["Date"], errors="coerce"
    )

    df["CPI"] = pd.to_numeric(
        df["CPI"], errors="coerce"
    )

    # Remove missing or invalid observations
    df = df.dropna(subset=["Date", "CPI"])

    # Standardize dates to the first of each month
    df["Date"] = (
        df["Date"].dt.to_period("M").dt.to_timestamp()
    )

    # Sort data chronologically
    df = df.sort_values("Date")

    # Remove duplicate months
    df = df.drop_duplicates(subset=["Date"], keep="last")

    # Ensure CPI values are positive
    df = df[df["CPI"] > 0]

    df = df.reset_index(drop=True)

    if df.empty:
        raise ValueError("No valid CPI observations were found.")

    # Calculate annual percentage change
    df["Annual Change"] = (
        (df["CPI"] / df["CPI"].shift(12)) - 1
    ) * 100

    print("CPI data successfully loaded.")

    print(
        "Available dates:",
        df["Date"].min().strftime("%B %Y"),
        "to",
        df["Date"].max().strftime("%B %Y")
    )

    return df


#creates graph

def create_graph(df):

    # Create images folder if it does not exist
    Path("images").mkdir(exist_ok=True)

    # Create first axis
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot CPI
    ax1.plot(
        df["Date"],
        df["CPI"],
        color="blue",
        label="Consumer Price Index (CPI)"
    )

    # Add base level
    ax1.axhline(
        y=100,
        color="black",
        linestyle=":",
        label="2002 Base Level (100)"
    )

    ax1.set_xlabel("Year")
    ax1.set_ylabel("CPI (2002 = 100)")

    ax1.set_title(
        "Canadian Consumer Price Index and Annual Inflation Rate"
    )

    # Create second axis
    ax2 = ax1.twinx()

    # Plot annual percentage change
    ax2.plot(
        df["Date"],
        df["Annual Change"],
        color="red",
        alpha=0.7,
        label="Annual Percentage Change"
    )

    ax2.set_ylabel("Annual Percentage Change (%)")

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(
        lines1 + lines2,
        labels1 + labels2,
        loc="upper left"
    )

    # Improve layout
    fig.tight_layout()

    # Save graph
    plt.savefig(
        "images/cpi_graph.png",
        dpi=300,
        bbox_inches="tight"
    )

    print("CPI graph saved to images/cpi_graph.png")

    # Save graph
    plt.savefig(
    "images/cpi_graph.png",
    dpi=300,
    bbox_inches="tight"
)

    print("CPI graph saved to images/cpi_graph.png")

    # Display graph
    plt.show()


# price input

def get_price():

    while True:

        try:
            price_input = input(
                "\nEnter the original price in CAD: $"
            )

            # Allow commas and dollar signs
            price_input = (
                price_input.replace(",", "")
                .replace("$", "")
                .strip()
            )

            price = float(price_input)

            if price <= 0:
                print("Price must be greater than zero.")
                continue

            return price

        except ValueError:
            print("Invalid price. Please enter a number.")


# 5. VALIDATE DATE INPUT

def get_date(prompt, df):

    earliest_date = df["Date"].min()
    latest_date = df["Date"].max()

    while True:

        date_input = input(prompt)

        try:
            date = datetime.strptime(
                date_input, "%Y-%m"
            )

            date = pd.Timestamp(date)

            # Check date against dataset
            if date < earliest_date or date > latest_date:

                print(
                    "Date is outside the available CPI data."
                )

                print(
                    "Available range:",
                    earliest_date.strftime("%Y-%m"),
                    "to",
                    latest_date.strftime("%Y-%m")
                )

                continue

            # Check whether exact month exists
            if not (df["Date"] == date).any():

                print(
                    "No CPI information is available for this month."
                )

                continue

            return date

        except ValueError:

            print(
                "Invalid date format. Please use YYYY-MM."
            )


# 6. INFLATION CALCULATOR

def inflation_calculator(df):

    print("\n========================================")
    print("       CANADIAN INFLATION CALCULATOR")
    print("========================================")

    # Obtain inputs
    price = get_price()

    date1 = get_date(
        "\nEnter the first date (YYYY-MM): ",
        df
    )

    date2 = get_date(
        "Enter the second date (YYYY-MM): ",
        df
    )

    # Retrieve CPI values
    cpi1 = float(
        df.loc[df["Date"] == date1, "CPI"].iloc[0]
    )

    cpi2 = float(
        df.loc[df["Date"] == date2, "CPI"].iloc[0]
    )

    # Calculate adjusted price
    adjusted_price = price * (cpi2 / cpi1)

    # Calculate percentage change
    percentage_change = (
        (adjusted_price - price) / price
    ) * 100

    # Calculate number of months
    months = (
        (date2.year - date1.year) * 12
        + date2.month - date1.month
    )

    # Calculate number of years
    years = months / 12

    # Calculate average annual inflation rate
    if months != 0:

        annual_rate = (
            (cpi2 / cpi1) ** (12 / months) - 1
        ) * 100

    else:
        annual_rate = 0

    # Determine whether prices increased or decreased
    if percentage_change > 0:
        change_description = "increase"
    elif percentage_change < 0:
        change_description = "decrease"
    else:
        change_description = "no change"

    # Display results
    print("\n========================================")
    print("          CALCULATION RESULTS")
    print("========================================")

    print(
        f"\nOriginal price: ${price:,.2f} CAD"
        f" in {date1.strftime('%B %Y')}"
    )

    print(
        f"Adjusted price: ${adjusted_price:,.2f} CAD"
        f" in {date2.strftime('%B %Y')}"
    )

    print(
        f"\nPercentage change: {abs(percentage_change):.2f}%"
        f" {change_description}"
    )

    print(f"Number of years: {years:.2f}")

    print(
        f"Average annual inflation rate: "
        f"{annual_rate:.2f}%"
    )

    print(f"\nCPI for first date: {cpi1:.2f}")

    print(f"CPI for second date: {cpi2:.2f}")

    print("\n2002 CPI (base level) = 100.00")

    print("========================================")


# 7. MAIN PROGRAM

def main():

    try:

        # Load CPI data
        df = load_data()

        # Create CPI graph
        create_graph(df)

        # Run calculator
        inflation_calculator(df)

    except FileNotFoundError as error:

        print(error)

    except ValueError as error:

        print("Data error:", error)


# Run program
if __name__ == "__main__":

    main()


