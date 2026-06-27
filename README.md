# R12. Redis-MySQL Consistency Auditor & Visualizer

## Problem Statement
In high-speed systems, Redis cache can fall out of sync with MySQL, leading to phantom states and data inconsistencies. This tool acts as an auditor to check and visualize data drift.

## Installation & Setup
1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install redis pymysql numpy matplotlib
