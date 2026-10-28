---
topic: "Trading Domain"
---
# Trading Domain

Market structure and trading-system concepts a quant developer is expected to know.

## Order Books 101 · Easy

What are the bid, ask, spread and depth in a limit order book?

### Answer

The bid is the highest price someone is willing to buy at, the ask (offer) the lowest price someone is willing to sell at. The spread is ask minus bid, and the mid price is their average. Depth is the quantity resting at each price level, showing how much can trade before the price moves.

## Order Types · Easy

Explain market, limit, IOC and FOK orders.

### Answer

A market order trades immediately at the best available prices, with no price guarantee. A limit order trades only at its limit price or better and rests in the book if it cannot fill. Immediate-or-Cancel fills whatever it can right now at its limit and cancels the rest; it never rests. Fill-or-Kill must fill completely immediately or is cancelled in full.

## Price-Time Priority · Easy

How does a price-time priority (FIFO) matching engine decide which resting orders fill first?

### Answer

Better price always first: highest bid, lowest ask. Among orders at the same price, the one that arrived earliest fills first. Modifying an order usually loses its time priority if the price changes or the size increases, while reducing size typically keeps it. Some markets (e.g. certain futures) use pro-rata allocation at a price level instead.

## Maker vs Taker · Easy

What is the difference between a maker and a taker, and why do fees differ?

### Answer

A maker posts a resting order that adds liquidity to the book; a taker sends an order that executes against resting orders, removing liquidity. Many exchanges charge takers a fee and pay makers a rebate (maker-taker model) to reward liquidity provision. Fee and rebate levels can decide whether a strategy is profitable.

## Market Maker Role · Medium

What does a market maker do, how does it earn money, and what is inventory risk?

### Answer

It continuously quotes both a bid and an ask, earning the spread (and often rebates) when both sides get filled. Inventory risk is that it ends up holding a position, e.g. long after selling flow hits its bid, and the price then moves against it. Market makers manage this by skewing quotes to attract offsetting trades, widening spreads, hedging in correlated instruments and limiting position size. They also face adverse selection from better-informed traders.

## Latency Arbitrage · Medium

What is latency arbitrage?

### Answer

Profiting from seeing a price change before others can react: e.g. a futures price moves on one exchange and a fast trader hits stale quotes on a related instrument elsewhere before the quoting firm can update them. The same trade is available to everyone, so the profit goes to whoever is fastest, which drives investment in colocation, microwave links and FPGAs. For the market maker being picked off, it is the main source of adverse selection.

## FIX vs Binary Protocols · Medium

Compare FIX with binary exchange protocols such as OUCH and ITCH.

### Answer

FIX is a text tag=value protocol (e.g. `35=D|55=AAPL|`) that is standard and flexible but verbose and slow to parse. Binary protocols use fixed-layout messages with fixed-width fields, so encoding and decoding is a few loads and stores. Nasdaq's OUCH is a binary order-entry protocol, ITCH a binary market data feed. Low-latency firms use native binary protocols; FIX is common for slower flows, drop copies and brokers.

## Market Data Levels · Easy

What is the difference between L1, L2 and L3 market data?

### Answer

L1 is top of book: best bid and ask with sizes and the last trade. L2 is market-by-price: aggregated quantity at each price level to some depth. L3 is market-by-order: every individual order with its own add, modify, cancel and execute events, from which you can rebuild the full book including queue position.

## Order Lifecycle · Medium

Describe a typical order lifecycle from the trading system's side.

### Answer

The system sends New Order; the exchange answers with an acknowledgement (accepted, now live) or a reject. A live order can be partially filled and then filled, cancelled (send cancel, receive cancel ack) or replaced/modified (cancel-replace, possibly losing queue priority). The client tracks pending states such as "pending cancel", because a fill can still arrive after a cancel was sent.

## Pre-trade Risk Checks · Medium

What pre-trade risk checks does an order gateway perform, and why must they be fast?

### Answer

Before sending each order, check things like maximum order size and notional, price collars (price not too far from the market), position and exposure limits, order rate limits, duplicate orders and restricted symbols. Regulations (e.g. SEC Rule 15c3-5) require them for market access. They sit on the critical path of every order, so they must take nanoseconds, typically using precomputed limits and simple arithmetic, sometimes in FPGA.

## Smart Order Routing · Medium

What does a smart order router do?

### Answer

When the same instrument trades on several venues, the router decides where to send each order or slice: using consolidated book data, fees and rebates, fill probabilities, hidden liquidity and latency to each venue. It may split an order across venues and time the pieces so they arrive together, to avoid others seeing the first fill and moving the price elsewhere. It must also respect rules such as best-execution or trade-through protection.

## Slippage · Easy

What is slippage?

### Answer

The difference between the expected price of a trade (e.g. the price when the decision was made, or the mid) and the actual average execution price. It comes from latency, market impact of your own order walking the book, and price movement. Execution quality is often measured as slippage versus an arrival-price benchmark.

## VWAP and TWAP · Medium

What are VWAP and TWAP execution algorithms?

### Answer

Both break a large parent order into small child orders to reduce market impact. TWAP spreads them evenly over time. VWAP trades in proportion to the expected volume profile (e.g. more at the open and close), aiming for an average price close to the market's volume-weighted average price, VWAP = Σ(price × volume) / Σ volume. They are benchmarks as well as algorithms.

## Realised vs Unrealised PnL · Easy

You buy 100 shares at 10, buy 100 more at 12, then sell 100 at 13. The price is now 14. Using average cost, what are realised and unrealised PnL?

### Answer

Average cost is 11. Realised PnL = 100 × (13 − 11) = 200. Unrealised PnL on the remaining 100 shares = 100 × (14 − 11) = 300, total 500. Realised PnL is locked in by closing trades; unrealised is marked to the current price and can still change. (FIFO accounting would split it 300 realised and 200 unrealised with the same total.)

## Position Limits · Easy

What are position limits, and where are they enforced?

### Answer

Caps on how large a position (in shares, contracts or notional) a strategy, desk or firm may hold, set by internal risk and sometimes by exchanges or regulators. They are enforced pre-trade by counting both current position and open orders that could fill, so a burst of orders cannot overshoot. Breaching them typically blocks new risk-increasing orders.

## Kill Switch · Medium

What is a kill switch in a trading system?

### Answer

A mechanism that instantly stops a strategy or the whole firm from trading: cancel all open orders and block new ones. It can be triggered manually or automatically by limits on loss, order rate, position or message errors. Many exchanges also offer cancel-on-disconnect and their own kill switches. Knight Capital's 2012 loss of about $440m in 45 minutes is the classic example of why it is needed.

## Tick Size · Easy

What is the tick size, and how does it affect trading?

### Answer

The minimum price increment an instrument can be quoted in, e.g. $0.01 for most US stocks above $1. A large tick relative to price makes the spread often one tick wide and creates long queues at each level, so queue position and speed matter a lot. A small tick lets traders step ahead of each other cheaply, so quotes change more often.

## Opening and Closing Auctions · Medium

How do opening and closing auctions work?

### Answer

Orders are collected for a period without matching, while the exchange publishes the indicative price and imbalance. At the uncross, the exchange picks the single price that maximises executed volume (with tie-break rules on imbalance and reference price), and all crossing orders trade at that price. The closing auction sets the official closing price used by index funds and for marking, so it is often a large share of daily volume.

## Colocation · Easy

What is colocation, and why do trading firms pay for it?

### Answer

Placing your servers in the exchange's data centre, close to the matching engine. It cuts network latency from milliseconds to microseconds. Exchanges usually equalise cable lengths inside the facility so that all colocated customers get the same distance to the engine.

## Order Book Data Structure · Hard

How would you design an order book data structure for a market-by-order feed, and what operations must be fast?

### Answer

Handle add, cancel, modify and execute by order id, and best bid/ask queries, all in O(1) or close. A common design is a hash map from order id to order node, price levels holding an intrusive doubly linked list of orders in time order, and the levels per side kept in a sorted structure; because most activity is near the top, an array indexed by price ticks around the mid is often fastest. Preallocate nodes from pools so there is no heap allocation.
