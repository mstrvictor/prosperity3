# Prosperity

## Installation

If the script './test' is not runnable 

```bash
chmod +x test
```

## Usage

After updating auto.py run ./test and it will run the backtesting and save the logs and scripts

Backtest on round 1 day 0 data and automatically open visualiser
```bash
./test 1-0 --vis
```

Backtest using data from all days from round 1 and automatically open visualiser
```bash
./test 1 --vis
```

Backtest using data from all days from round 1 and merge pnl across days
```bash
./test 1 --merge-pnl
```

If no args are given it will fun
```bash
./test 1 --merge-pnl --vis
```
