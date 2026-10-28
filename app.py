import math

import altair as alt
import numpy as np
import streamlit as st

from engine import black_scholes


st.set_page_config(
    page_title="Option Analytics | Black–Scholes",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f3f6fb 0%, #fbfcfe 280px);
    }
    [data-testid="stSidebarContent"] {
        padding-top: 1rem;
    }
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e6ebf2;
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 2px 8px rgba(20, 40, 70, 0.04);
    }
    [data-testid="stMetricLabel"] {
        color: #64748b;
    }
    h1,
    [data-testid="stTitle"] h1 {
        color: #0f172a !important;
        font-size: 2.5rem;
        font-weight: 750;
        letter-spacing: -0.03em;
        margin-bottom: 0.35rem;
    }
    [data-theme="dark"] h1,
    [data-theme="dark"] [data-testid="stTitle"] h1 {
        color: #f8fafc !important;
    }
    .app-intro {
        color: #475569;
        font-size: 1.05rem;
        line-height: 1.6;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    [data-theme="dark"] .app-intro {
        color: #cbd5e1;
    }
    .overview-heading {
        color: #0f172a !important;
        font-size: 1.55rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        line-height: 1.3;
        margin: 0 0 0.35rem;
    }
    [data-theme="dark"] .overview-heading {
        color: #f8fafc !important;
    }
    .overview-details {
        color: #475569 !important;
        font-size: 0.875rem;
        line-height: 1.5;
        margin: 0 0 1rem;
    }
    [data-theme="dark"] .overview-details {
        color: #cbd5e1 !important;
    }
    [data-testid="stMetricValue"] {
        color: #0f172a;
        font-size: 2rem;
        font-weight: 700;
    }
    [data-theme="dark"] [data-testid="stMetricValue"] {
        color: #f8fafc;
    }
    .st-key-option_chart_section h3,
    .st-key-what_if_simulator h3,
    .st-key-option_chart_section [data-testid="stCaptionContainer"] p,
    .st-key-what_if_simulator [data-testid="stCaptionContainer"] p,
    .st-key-what_if_simulator [data-testid="stWidgetLabel"],
    .st-key-what_if_simulator [data-testid="stWidgetLabel"] p {
        color: #334155 !important;
    }
    .st-key-option_chart_section h3,
    .st-key-what_if_simulator h3 {
        color: #0f172a !important;
        font-weight: 700;
    }
    [data-theme="dark"] .st-key-option_chart_section h3,
    [data-theme="dark"] .st-key-what_if_simulator h3,
    [data-theme="dark"] .st-key-option_chart_section [data-testid="stCaptionContainer"] p,
    [data-theme="dark"] .st-key-what_if_simulator [data-testid="stCaptionContainer"] p,
    [data-theme="dark"] .st-key-what_if_simulator [data-testid="stWidgetLabel"],
    [data-theme="dark"] .st-key-what_if_simulator [data-testid="stWidgetLabel"] p {
        color: #e2e8f0 !important;
    }
    .st-key-what_if_simulator [data-testid="stMetricLabel"],
    .st-key-what_if_simulator [data-testid="stMetricLabel"] *,
    .st-key-what_if_simulator [data-testid="stMetricValue"],
    .st-key-what_if_simulator [data-testid="stMetricValue"] * {
        color: #0f172a !important;
    }
    .simulator-greeks-heading {
        color: #0f172a !important;
        font-size: 1.25rem;
        font-weight: 700;
        margin: 0 0 0.6rem;
    }
    .simulator-greeks {
        color: #334155 !important;
        line-height: 1.65;
        margin: 0;
        padding-left: 1.35rem;
    }
    .simulator-greeks strong {
        color: #0f172a !important;
    }
    .projection-interpretation {
        color: #334155 !important;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-top: 0.75rem;
    }
    .projection-interpretation strong {
        color: #0f172a !important;
    }
    [data-theme="dark"] .st-key-what_if_simulator [data-testid="stMetricLabel"],
    [data-theme="dark"] .st-key-what_if_simulator [data-testid="stMetricLabel"] *,
    [data-theme="dark"] .st-key-what_if_simulator [data-testid="stMetricValue"],
    [data-theme="dark"] .st-key-what_if_simulator [data-testid="stMetricValue"] * {
        color: #0f172a !important;
    }
    [data-theme="dark"] .simulator-greeks-heading,
    [data-theme="dark"] .simulator-greeks,
    [data-theme="dark"] .simulator-greeks strong {
        color: #f8fafc !important;
    }
    [data-theme="dark"] .projection-interpretation,
    [data-theme="dark"] .projection-interpretation strong {
        color: #e2e8f0 !important;
    }
    .personal-attribution {
        color: #64748b;
        font-size: 0.8rem;
        line-height: 1.5;
        margin: 1.1rem 0 0;
        text-align: left;
    }
    main .block-container:has(.personal-attribution) {
        padding-bottom: 0.75rem !important;
    }
    div[data-testid="stMarkdown"]:has(.personal-attribution) {
        margin-bottom: 0 !important;
    }
    .personal-attribution strong {
        color: #334155;
        font-weight: 600;
    }
    .personal-attribution a {
        color: #475569;
        text-decoration: underline;
        text-decoration-color: #94a3b8;
        text-underline-offset: 2px;
    }
    .personal-attribution a:hover {
        color: #0e7490;
        text-decoration-color: currentColor;
    }
    [data-theme="dark"] .personal-attribution,
    [data-theme="dark"] .personal-attribution strong,
    [data-theme="dark"] .personal-attribution a {
        color: #cbd5e1;
    }
    [data-theme="dark"] .personal-attribution a {
        text-decoration-color: #64748b;
    }
    .difference-card {
        background: #ffffff;
        border: 1px solid #e6ebf2;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(20, 40, 70, 0.04);
    }
    [data-theme="dark"] .difference-card {
        background: #1e293b;
        border-color: #334155;
    }
    .difference-label {
        color: #64748b;
        font-size: 0.875rem;
        margin-bottom: 8px;
    }
    .difference-values {
        display: grid;
        grid-template-columns: minmax(0, 1.4fr) minmax(0, 0.8fr);
        align-items: center;
        gap: 8px;
    }
    .difference-primary {
        color: #0f172a;
        font-size: clamp(1.05rem, 2.2vw, 1.6rem);
        font-weight: 700;
        line-height: 1.25;
        overflow-wrap: anywhere;
    }
    [data-theme="dark"] .difference-primary {
        color: #f8fafc;
    }
    .difference-percent {
        font-size: clamp(0.9rem, 1.8vw, 1.15rem);
        font-weight: 600;
        line-height: 1.25;
        text-align: right;
        overflow-wrap: anywhere;
    }
    .difference-positive {
        color: #16803c;
    }
    [data-theme="dark"] .difference-positive {
        color: #4ade80;
    }
    .difference-negative {
        color: #c62828;
    }
    [data-theme="dark"] .difference-negative {
        color: #f87171;
    }
    .difference-neutral {
        color: #64748b;
    }
    [data-theme="dark"] .difference-neutral {
        color: #cbd5e1;
    }
    @media (max-width: 640px) {
        .difference-card {
            padding: 12px;
        }
        .difference-values {
            grid-template-columns: minmax(0, 1.25fr) minmax(0, 0.75fr);
            gap: 6px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Options analytics")
st.markdown(
    '<p class="app-intro">Explore a European option&#39;s theoretical value and '
    "sensitivity to key market inputs.</p>",
    unsafe_allow_html=True,
)
st.info(
    "**Model estimate only:** This is a theoretical Black–Scholes value, not a live "
    "market quote or a guaranteed fair value. Actual prices can differ."
)

with st.sidebar:
    st.header("Option inputs")
    st.caption("Enter market assumptions to update the analysis.")

    stock_price = st.number_input(
        "Stock price ($)",
        min_value=0.01,
        value=100.00,
        step=1.00,
        format="%.2f",
        help="Current price of the underlying stock.",
    )
    strike_price = st.number_input(
        "Strike price ($)",
        min_value=0.01,
        value=100.00,
        step=1.00,
        format="%.2f",
        help="Price at which the option can be exercised.",
    )
    days_to_expiration = st.number_input(
        "Days to expiration",
        min_value=1,
        value=30,
        step=1,
        help="Time remaining until expiration, in calendar days.",
    )
    annual_rate_pct = st.number_input(
        "Annual risk-free rate (%)",
        min_value=-100.0,
        max_value=100.0,
        value=4.5,
        step=0.25,
        format="%.2f",
        help="Annualized risk-free interest-rate assumption.",
    )
    annual_volatility_pct = st.number_input(
        "Annualized volatility (%)",
        min_value=0.1,
        max_value=500.0,
        value=25.0,
        step=1.0,
        format="%.2f",
        help="Expected annualized standard deviation of stock returns.",
    )
    option_type_label = st.radio("Option type", ("Call", "Put"), horizontal=True)

# The engine expects time in years and rates/volatility as decimals, not percentages.
time_to_expiration = days_to_expiration / 365.0
risk_free_rate = annual_rate_pct / 100.0
volatility = annual_volatility_pct / 100.0
option_type = option_type_label.lower()

numeric_inputs = (
    stock_price,
    strike_price,
    time_to_expiration,
    risk_free_rate,
    volatility,
)
if not all(math.isfinite(value) for value in numeric_inputs):
    st.error("Please enter finite numeric values for all option inputs.")
    st.stop()

try:
    result = black_scholes(
        stock_price,
        strike_price,
        time_to_expiration,
        risk_free_rate,
        volatility,
        option_type=option_type,
    )
except ValueError as error:
    st.error(f"Unable to calculate this option: {error}")
    st.stop()

st.markdown(
    f'<h3 class="overview-heading">{option_type_label} option overview</h3>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<p class="overview-details">${stock_price:,.2f} stock · '
    f'${strike_price:,.2f} strike · {days_to_expiration} calendar days · '
    f'{annual_rate_pct:.2f}% rate · {annual_volatility_pct:.2f}% volatility</p>',
    unsafe_allow_html=True,
)

price_column, delta_column, gamma_column = st.columns(3)
price_column.metric("Theoretical option price", f"${result['price']:,.2f}")
delta_column.metric("Delta", f"{result['delta']:.4f}")
gamma_column.metric("Gamma", f"{result['gamma']:.6f}")

theta_per_day = result["theta_per_year"] / 365.0
theta_column, vega_column, rho_column = st.columns(3)
theta_column.metric("Theta / calendar day", f"${theta_per_day:,.4f}")
vega_column.metric("Vega / 1 vol point", f"${result['vega_per_1_vol_point']:,.4f}")
rho_column.metric("Rho / 1 rate point", f"${result['rho_per_1_rate_point']:,.4f}")

st.divider()
chart_column, simulator_column = st.columns((1.7, 1))

with chart_column.container(key="option_chart_section"):
    st.subheader("Projected option return by stock price")
    st.caption(
        "Returns are relative to the original option premium; the dotted line "
        "marks 0% return (the original cost)."
    )
    chart_placeholder = st.empty()
    stock_prices = np.linspace(stock_price * 0.5, stock_price * 1.5, 51)
    chart_line = None
with simulator_column.container(key="what_if_simulator"):
    st.subheader("What-If Simulator")
    st.caption("Adjust stock price and time; all other main inputs stay fixed.")
    hypothetical_stock_price = st.number_input(
        "Hypothetical stock price ($)",
        min_value=0.01,
        value=float(stock_price),
        step=1.00,
        format="%.2f",
        help="Stock price assumption for this what-if estimate.",
    )
    hypothetical_days = st.number_input(
        "Days until expiration (DTE)",
        min_value=1,
        value=int(days_to_expiration),
        step=1,
        help="Calendar days remaining in this what-if scenario.",
    )
    iv_change_std_points = st.number_input(
        "IV change standard deviation (percentage points)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.5,
        format="%.1f",
        help=(
            "Manual one-standard-deviation change in implied volatility, expressed "
            "in percentage points (for example, 5 means a move from 32% to 37%)."
        ),
    )
    evaluation_days = st.number_input(
        "Projection date (days from today)",
        min_value=0,
        max_value=365,
        value=0,
        step=1,
        help=(
            "Days elapsed before the projected valuation. Remaining model time is "
            "simulator DTE minus this value; it must be less than simulator DTE."
        ),
    )
    st.caption(
        "No historical IV series is available, so the IV change is a manual "
        "assumption, not a statistical confidence interval or 68% probability range."
    )

    hypothetical_result = None
    projection_description = None
    if result["price"] <= 0:
        st.error("Cannot calculate returns because the original option premium is zero.")
    elif evaluation_days >= hypothetical_days:
        st.error("The projection date must be before the simulator's expiration.")
    elif hypothetical_days - evaluation_days > days_to_expiration:
        st.error(
            "Projected remaining DTE cannot exceed the original option's DTE."
        )
    else:
        # Keep projected IV positive for the pricing engine and cap all scenarios at 100%.
        base_iv_pct = min(annual_volatility_pct, 100.0)
        high_iv_pct = min(base_iv_pct + iv_change_std_points, 100.0)
        low_iv_pct = max(base_iv_pct - iv_change_std_points, 0.01)
        remaining_dte = hypothetical_days - evaluation_days
        elapsed_days = days_to_expiration - remaining_dte
        projection_time = remaining_dte / 365.0
        scenario_volatilities = (
            ("Base IV", base_iv_pct),
            ("High IV", high_iv_pct),
            ("Low IV", low_iv_pct),
        )
        def price_projection(projected_stock_price, scenario_iv_pct):
            return black_scholes(
                projected_stock_price,
                strike_price,
                projection_time,
                risk_free_rate,
                scenario_iv_pct / 100.0,
                option_type=option_type,
            )

        projection_stock_prices = stock_prices
        if (
            math.isfinite(hypothetical_stock_price)
            and stock_prices[0] <= hypothetical_stock_price <= stock_prices[-1]
        ):
            # Include the marker's x-coordinate so it lies on the rendered base curve.
            projection_stock_prices = np.sort(
                np.append(stock_prices, hypothetical_stock_price)
            )
        st.caption(
            "Scenario IVs (percentage points): "
            f"base {base_iv_pct:.2f}%, high {high_iv_pct:.2f}%, low {low_iv_pct:.2f}%. "
            "Values are constrained to 0.01%–100%; the positive floor is required "
            "by the pricing engine."
        )
        try:
            hypothetical_result = price_projection(
                hypothetical_stock_price,
                base_iv_pct,
            )
            high_iv_estimate = price_projection(
                hypothetical_stock_price,
                high_iv_pct,
            )
            low_iv_estimate = price_projection(
                hypothetical_stock_price,
                low_iv_pct,
            )
            projected_return_pct = (
                hypothetical_result["price"] / result["price"] - 1
            ) * 100
            high_iv_return_pct = (
                high_iv_estimate["price"] / result["price"] - 1
            ) * 100
            low_iv_return_pct = (
                low_iv_estimate["price"] / result["price"] - 1
            ) * 100
            direction = (
                "rises"
                if hypothetical_stock_price > stock_price
                else "falls"
                if hypothetical_stock_price < stock_price
                else "stays at"
            )
            projection_description = (
                f"If the stock {direction} from ${stock_price:,.2f} to "
                f"${hypothetical_stock_price:,.2f}, the {option_type_label.lower()} "
                f"with a ${strike_price:,.2f} strike, originally priced with "
                f"{days_to_expiration} days to expiration at ${result['price']:,.2f} "
                f"per share, is estimated at ${hypothetical_result['price']:,.2f} "
                f"after {elapsed_days} elapsed days "
                f"({remaining_dte} days remaining). That is a "
                f"{projected_return_pct:+.2f}% return relative to the original "
                f"premium. The base case uses {base_iv_pct:.2f}% IV; at "
                f"{high_iv_pct:.2f}% high IV, the estimate is "
                f"${high_iv_estimate['price']:,.2f} ({high_iv_return_pct:+.2f}% "
                f"return), while {low_iv_pct:.2f}% low IV gives "
                f"${low_iv_estimate['price']:,.2f} ({low_iv_return_pct:+.2f}% "
                "return). These are theoretical estimates, not guaranteed future "
                "market prices."
            )
            projection_data = []
            for scenario_name, scenario_iv_pct in scenario_volatilities:
                for price in projection_stock_prices:
                    projected_result = price_projection(
                        float(price),
                        scenario_iv_pct,
                    )
                    projection_data.append(
                        {
                            "Stock price ($)": float(price),
                            "Theoretical option value ($)": float(
                                projected_result["price"]
                            ),
                            "Projected return (%)": (
                                projected_result["price"] / result["price"] - 1
                            )
                            * 100,
                            "IV scenario": scenario_name,
                            "Assumed IV (%)": scenario_iv_pct,
                            "Remaining DTE (days)": remaining_dte,
                        }
                    )
        except ValueError as error:
            hypothetical_result = None
            st.error(f"Unable to build the IV sensitivity projections: {error}")
        else:
            chart_line = alt.Chart(
                data=alt.Data(values=projection_data)
            ).mark_line(
                strokeWidth=2.5,
            ).encode(
                x=alt.X("Stock price ($):Q", title="Stock price ($)"),
                y=alt.Y("Projected return (%):Q", title="Return vs. original premium (%)"),
                color=alt.Color(
                    "IV scenario:N",
                    title="IV scenario",
                    scale=alt.Scale(
                        domain=["Base IV", "High IV", "Low IV"],
                        range=["#2563eb", "#d97706", "#7c3aed"],
                    ),
                    legend=alt.Legend(orient="top", direction="horizontal"),
                ),
                tooltip=[
                    alt.Tooltip("IV scenario:N", title="Scenario"),
                    alt.Tooltip("Stock price ($):Q", format="$.2f"),
                    alt.Tooltip(
                        "Theoretical option value ($):Q",
                        title="Projected option value",
                        format="$.2f",
                    ),
                    alt.Tooltip("Projected return (%):Q", format="+.2f"),
                    alt.Tooltip("Assumed IV (%):Q", format=".2f"),
                    alt.Tooltip("Remaining DTE (days):Q", format=".0f"),
                ],
            )
            # A nearly transparent wider stroke enlarges line hit targets without
            # changing the visible series thickness or styling.
            line_hover_targets = alt.Chart(
                data=alt.Data(values=projection_data)
            ).mark_line(
                strokeWidth=8,
                opacity=0.001,
            ).encode(
                x="Stock price ($):Q",
                y="Projected return (%):Q",
                color=alt.Color(
                    "IV scenario:N",
                    scale=alt.Scale(
                        domain=["Base IV", "High IV", "Low IV"],
                        range=["#2563eb", "#d97706", "#7c3aed"],
                    ),
                    legend=None,
                ),
                detail="IV scenario:N",
                tooltip=[
                    alt.Tooltip("IV scenario:N", title="Scenario"),
                    alt.Tooltip("Stock price ($):Q", format="$.2f"),
                    alt.Tooltip(
                        "Theoretical option value ($):Q",
                        title="Projected option value",
                        format="$.2f",
                    ),
                    alt.Tooltip("Projected return (%):Q", format="+.2f"),
                    alt.Tooltip("Assumed IV (%):Q", format=".2f"),
                    alt.Tooltip("Remaining DTE (days):Q", format=".0f"),
                ],
            )
            chart_line = chart_line + line_hover_targets
            original_cost_data = [
                {
                    "Stock price ($)": float(stock_prices[0]),
                    "Projected return (%)": 0.0,
                    "Label": f"Original cost: ${result['price']:.2f}",
                }
            ]
            original_cost_rule = alt.Chart(
                data=alt.Data(values=original_cost_data)
            ).mark_rule(
                color="#0e7490",
                strokeDash=[2, 4],
                strokeWidth=2,
            ).encode(
                y="Projected return (%):Q",
                tooltip=[
                    alt.Tooltip("Label:N", title="Reference"),
                    alt.Tooltip("Projected return (%):Q", format=".2f"),
                ],
            )
            original_cost_label = alt.Chart(
                data=alt.Data(values=original_cost_data)
            ).mark_text(
                align="left",
                baseline="bottom",
                color="#0e7490",
                dx=8,
                dy=-5,
                fontSize=12,
            ).encode(
                x="Stock price ($):Q",
                y="Projected return (%):Q",
                text="Label:N",
            )
            chart_line = chart_line + original_cost_rule + original_cost_label

    if not math.isfinite(hypothetical_stock_price):
        st.error("Enter a finite hypothetical stock price.")
    elif hypothetical_result is not None:
        st.caption("Theoretical estimate only — not a live market quote.")
        value_column, contract_column = st.columns(2)
        value_column.metric(
            "Option value / share",
            f"${hypothetical_result['price']:,.2f}",
        )
        contract_column.metric(
            "Option value / 100 shares",
            f"${hypothetical_result['price'] * 100:,.2f}",
        )

        price_difference = hypothetical_result["price"] - result["price"]
        if result["price"] == 0:
            percentage_difference = "N/A (original price is $0.00)"
        else:
            percentage_difference = (
                f"{price_difference / result['price'] * 100:+.2f}%"
            )
        difference_color = (
            "difference-positive"
            if price_difference > 0
            else "difference-negative"
            if price_difference < 0
            else "difference-neutral"
        )
        st.markdown(
            f"""
            <div class="difference-card">
                <div class="difference-label">Difference vs. original price</div>
                <div class="difference-values">
                    <div class="difference-primary">${price_difference:+,.2f} / share</div>
                    <div class="difference-percent {difference_color}">{percentage_difference}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        greek_column_1, greek_column_2 = st.columns(2)
        greek_column_1.metric("Delta", f"{hypothetical_result['delta']:.4f}")
        greek_column_2.metric("Gamma", f"{hypothetical_result['gamma']:.6f}")
        greek_column_1.metric(
            "Theta / calendar day",
            f"${hypothetical_result['theta_per_year'] / 365:,.4f}",
        )
        greek_column_2.metric(
            "Vega / 1 vol point",
            f"${hypothetical_result['vega_per_1_vol_point']:,.4f}",
        )
        greek_column_1.metric(
            "Rho / 1 rate point",
            f"${hypothetical_result['rho_per_1_rate_point']:,.4f}",
        )

        # Use the same base-case result as the displayed simulator estimate.
        if (
            chart_line is not None
            and stock_prices[0] <= hypothetical_stock_price <= stock_prices[-1]
        ):
            marker_data = [
                {
                    "Stock price ($)": float(hypothetical_stock_price),
                    "Projected return (%)": (
                        hypothetical_result["price"] / result["price"] - 1
                    )
                    * 100,
                    "Scenario": "Base IV estimate",
                    "Theoretical option value ($)": float(
                        hypothetical_result["price"]
                    ),
                    "Assumed IV (%)": base_iv_pct,
                    "Remaining DTE (days)": remaining_dte,
                }
            ]
            marker = alt.Chart(data=alt.Data(values=marker_data)).mark_point(
                color="#e4572e",
                filled=True,
                size=100,
            ).encode(
                x="Stock price ($):Q",
                y="Projected return (%):Q",
                tooltip=[
                    "Scenario:N",
                    alt.Tooltip("Stock price ($):Q", format="$.2f"),
                    alt.Tooltip("Theoretical option value ($):Q", format="$.2f"),
                    alt.Tooltip("Projected return (%):Q", format="+.2f"),
                    alt.Tooltip("Assumed IV (%):Q", format=".2f"),
                    alt.Tooltip("Remaining DTE (days):Q", format=".0f"),
                ],
            )
            chart_line = chart_line + marker
if chart_line is not None:
    # This tall chart balances the simulator metrics and Greek explanations beside it.
    chart_placeholder.altair_chart(
        chart_line.properties(height=760),
        use_container_width=True,
    )
    if projection_description is not None:
        chart_column.markdown(
            '<div class="projection-interpretation">'
            "<strong>How to interpret this projection</strong><br>"
            f"{projection_description}"
            "</div>",
            unsafe_allow_html=True,
        )

assumptions_column, greeks_column = st.columns(2, vertical_alignment="center")
with assumptions_column:
    st.markdown(
        """
        <h3 class="simulator-greeks-heading">Model assumptions &amp; limitations</h3>
        <ul class="simulator-greeks">
            <li><strong>Pricing model:</strong> Black–Scholes for European options;
                the call or put type follows the calculator selection.</li>
            <li><strong>Implied volatility:</strong> Held constant within each
                individual projection scenario.</li>
            <li><strong>Interest rate and dividends:</strong> Uses the entered
                annual risk-free rate, continuously compounded. Dividend yield
                is not an input and is not included.</li>
            <li><strong>Limitations:</strong> Theoretical estimates are not
                guaranteed future prices. Actual prices may differ due to
                changing volatility, supply and demand, bid-ask spreads, and
                other market factors.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

with greeks_column:
    st.markdown(
        """
        <h3 class="simulator-greeks-heading">Understanding the Greeks</h3>
        <ul class="simulator-greeks">
            <li><strong>Delta</strong> — estimated option-price change for a <strong>$1</strong> stock-price move.</li>
            <li><strong>Gamma</strong> — how much Delta changes for a <strong>$1</strong> stock-price move.</li>
            <li><strong>Theta</strong> — estimated option-value change for <strong>one calendar day</strong> passing.</li>
            <li><strong>Vega</strong> — estimated price change for a <strong>1 percentage-point</strong> volatility move.</li>
            <li><strong>Rho</strong> — estimated price change for a <strong>1 percentage-point</strong> interest-rate move.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )
    st.caption(
        "Greeks are local sensitivities: they estimate the effect of a small change "
        "while other inputs are held constant."
    )

st.markdown(
    """
    <div class="personal-attribution">
        <strong>Built by Nick Sundquist</strong><br>
        University of Saskatchewan | B.Comm Student<br>
        <a href="https://www.linkedin.com/in/nick-sundquist"
           target="_blank" rel="noopener noreferrer">LinkedIn</a>
        &nbsp;·&nbsp;
        <a href="https://github.com/nicksundquist/black-scholes"
           target="_blank" rel="noopener noreferrer">GitHub</a>
    </div>
    """,
    unsafe_allow_html=True,
)