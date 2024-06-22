# Payslip Generation Web Application

## Overview

This project is a web application built using Python and Flask that generates a PDF payslip based on user-provided input. The application takes various details such as the organization name, employee details, bank details, annual income, and the month/year for which the payslip is being generated. The calculations for the salary components are performed according to the provided annual income, and the resulting payslip is formatted and displayed in a PDF file.

## Features

- Input form for organization, employee, and salary details.
- Monthly salary calculation based on provided annual income.
- Automatic tax and health insurance deductions.
- Generates a neatly formatted PDF payslip.
- Dropdown for selecting the month to ensure valid input.
- Customizable CSS for better styling.

## Calculations

The calculations for the payslip components are based on the following logic:

### Monthly Salary

The monthly salary is calculated by dividing the annual income by 12.

### Tax Calculation

The tax is calculated based on the current Indian tax slabs:

- Up to ₹2,50,000: No tax
- ₹2,50,001 to ₹5,00,000: 5%
- ₹5,00,001 to ₹7,50,000: 10%
- ₹7,50,001 to ₹10,00,000: 15%
- ₹10,00,001 to ₹12,50,000: 20%
- ₹12,50,001 to ₹15,00,000: 25%
- Above ₹15,00,000: 30%

### Health Insurance

Health insurance is assumed to be 2% of the monthly salary.

### Salary Components

The monthly salary is divided into the following components:

- Basic Salary: 50% of the monthly salary.
- House Rent Allowance (HRA): 30% of the monthly salary (capped at ₹5000).
- Adhoc Allowance: 15% of the monthly salary.
- Miscellaneous Allowance: 5% of the monthly salary.

If HRA exceeds ₹5000, the excess amount is added to the Basic Salary.

## Installation and Setup

### Prerequisites

- Python 3.x
- Flask
- ReportLab