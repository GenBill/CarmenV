CREATE TABLE IF NOT EXISTS daily_bars (
  date DATE,
  ticker VARCHAR,
  open DOUBLE,
  high DOUBLE,
  low DOUBLE,
  close DOUBLE,
  volume DOUBLE,
  amount DOUBLE,
  adj_factor DOUBLE,
  PRIMARY KEY (date, ticker)
);

CREATE TABLE IF NOT EXISTS technical_features (
  date DATE,
  ticker VARCHAR,
  close DOUBLE,
  ma5 DOUBLE,
  ma10 DOUBLE,
  ma20 DOUBLE,
  ma60 DOUBLE,
  return_1d DOUBLE,
  return_5d DOUBLE,
  return_20d DOUBLE,
  volatility_20d DOUBLE,
  amount_ma20 DOUBLE,
  atr_14 DOUBLE,
  relative_strength_20d DOUBLE,
  PRIMARY KEY (date, ticker)
);

CREATE TABLE IF NOT EXISTS candidates (
  date DATE,
  ticker VARCHAR,
  source VARCHAR,
  rank INTEGER,
  pattern_type VARCHAR,
  close DOUBLE,
  reason VARCHAR,
  feature_snapshot JSON,
  PRIMARY KEY (date, ticker, source)
);

CREATE TABLE IF NOT EXISTS agent_scores (
  date DATE,
  ticker VARCHAR,
  technical_score DOUBLE,
  narrative_score DOUBLE,
  fundamental_score DOUBLE,
  risk_score DOUBLE,
  liquidity_score DOUBLE,
  final_score DOUBLE,
  confidence DOUBLE,
  summary VARCHAR,
  raw_response VARCHAR,
  PRIMARY KEY (date, ticker)
);

CREATE TABLE IF NOT EXISTS trade_plans (
  date DATE,
  ticker VARCHAR,
  trade_type VARCHAR,
  entry_zone_low DOUBLE,
  entry_zone_high DOUBLE,
  stop_loss DOUBLE,
  take_profit_1 DOUBLE,
  take_profit_2 DOUBLE,
  invalid_condition VARCHAR,
  holding_period_days INTEGER,
  position_size_pct DOUBLE,
  reason VARCHAR,
  PRIMARY KEY (date, ticker)
);

CREATE TABLE IF NOT EXISTS forward_returns (
  date DATE,
  ticker VARCHAR,
  horizon_days INTEGER,
  entry_close DOUBLE,
  future_close DOUBLE,
  return_pct DOUBLE,
  max_drawdown_pct DOUBLE,
  max_runup_pct DOUBLE,
  hit_stop_loss BOOLEAN,
  PRIMARY KEY (date, ticker, horizon_days)
);

CREATE TABLE IF NOT EXISTS attribution_reviews (
  date DATE,
  ticker VARCHAR,
  actual_bought BOOLEAN,
  entry_price DOUBLE,
  exit_price DOUBLE,
  exit_reason VARCHAR,
  profit_loss_pct DOUBLE,
  attribution_tags VARCHAR,
  manual_comment VARCHAR,
  PRIMARY KEY (date, ticker)
);
