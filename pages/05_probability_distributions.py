import streamlit as st
import pandas as pd
from styles import apply_styles
from utils import render_formula, format_number
import distribution_functions as dist
import charts

apply_styles()

st.title("Probability Distributions")
st.warning("Note: Theoretical distributions do NOT automatically describe the metro data. They are mathematical models that may or may not fit the reality of ridership.")

dist_choice = st.sidebar.radio(
    "Select a Distribution:",
    ["Binomial", "Poisson", "Normal", "Exponential", "Uniform"]
)

if dist_choice == "Binomial":
    st.header("Binomial Distribution (Discrete)")
    st.markdown("Models the number of successes in a fixed number of independent trials, each with the same probability of success.")
    render_formula(
        r"P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}",
        {"n": "Number of trials (integer $\ge$ 1)", "p": "Probability of success in one trial (0 $\le$ p $\le$ 1)", "k": "Number of successes"}
    )
    
    with st.form("binom_form"):
        n = st.number_input("n (trials)", min_value=1, value=10, step=1)
        p = st.number_input("p (probability of success)", min_value=0.0, max_value=1.0, value=0.5)
        k = st.number_input("k (target successes)", min_value=0, max_value=n, value=5, step=1)
        submit = st.form_submit_button("Calculate Distribution")
        
    if submit:
        pmf, cdf = dist.calculate_binomial(n, p, k)
        st.success(f"**PMF ( P(X = {k}) )**: {format_number(pmf)}")
        st.info(f"**CDF ( P(X $\le$ {k}) )**: {format_number(cdf)}")
        
        df_plot = dist.generate_binomial_plot_data(n, p)
        fig = charts.plot_distribution_curve(df_plot, 'x', 'PMF', "Binomial PMF", is_discrete=True)
        st.plotly_chart(fig, use_container_width=True)

elif dist_choice == "Poisson":
    st.header("Poisson Distribution (Discrete)")
    st.markdown("Models the number of events occurring in a fixed interval of time or space, given a known constant mean rate of occurrence.")
    render_formula(
        r"P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}",
        {r"\lambda": "Average rate of events ($\lambda > 0$)", "k": "Number of events"}
    )
    
    with st.form("poisson_form"):
        lam = st.number_input(r"Lambda ($\lambda$)", min_value=0.01, value=5.0)
        k = st.number_input("k (target events)", min_value=0, value=5, step=1)
        submit = st.form_submit_button("Calculate Distribution")
        
    if submit:
        pmf, cdf = dist.calculate_poisson(lam, k)
        st.success(f"**PMF ( P(X = {k}) )**: {format_number(pmf)}")
        st.info(f"**CDF ( P(X $\le$ {k}) )**: {format_number(cdf)}")
        
        df_plot = dist.generate_poisson_plot_data(lam)
        fig = charts.plot_distribution_curve(df_plot, 'x', 'PMF', "Poisson PMF", is_discrete=True)
        st.plotly_chart(fig, use_container_width=True)

elif dist_choice == "Normal":
    st.header("Normal Distribution (Continuous)")
    st.markdown("Models data that clusters around a mean and is symmetric (the bell curve).")
    render_formula(
        r"f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}",
        {r"\mu": "Mean", r"\sigma": "Standard Deviation ($\sigma > 0$)", "x": "Value"}
    )
    
    with st.form("normal_form"):
        mu = st.number_input(r"Mean ($\mu$)", value=0.0)
        sigma = st.number_input(r"Standard Deviation ($\sigma$)", min_value=0.01, value=1.0)
        x = st.number_input("x (target value)", value=0.0)
        submit = st.form_submit_button("Calculate Distribution")
        
    if submit:
        pdf, cdf = dist.calculate_normal(mu, sigma, x)
        st.success(f"**PDF at x={x}**: {format_number(pdf)}")
        st.info(f"**CDF ( P(X $\le$ {x}) )**: {format_number(cdf)}")
        
        df_plot = dist.generate_normal_plot_data(mu, sigma)
        fig = charts.plot_distribution_curve(df_plot, 'x', 'PDF', "Normal PDF", is_discrete=False)
        st.plotly_chart(fig, use_container_width=True)

elif dist_choice == "Exponential":
    st.header("Exponential Distribution (Continuous)")
    st.markdown("Models the time between events in a Poisson point process (e.g., time between train arrivals).")
    render_formula(
        r"f(x) = \lambda e^{-\lambda x}",
        {r"\lambda": "Rate parameter ($\lambda > 0$)", "x": "Time or distance (x $\ge$ 0)"}
    )
    
    with st.form("exp_form"):
        lam = st.number_input(r"Rate ($\lambda$)", min_value=0.01, value=1.0)
        x = st.number_input("x (target value)", min_value=0.0, value=1.0)
        submit = st.form_submit_button("Calculate Distribution")
        
    if submit:
        scale = 1.0 / lam
        pdf, cdf = dist.calculate_exponential(scale, x)
        st.success(f"**PDF at x={x}**: {format_number(pdf)}")
        st.info(f"**CDF ( P(X $\le$ {x}) )**: {format_number(cdf)}")
        
        df_plot = dist.generate_exponential_plot_data(scale)
        fig = charts.plot_distribution_curve(df_plot, 'x', 'PDF', "Exponential PDF", is_discrete=False)
        st.plotly_chart(fig, use_container_width=True)

elif dist_choice == "Uniform":
    st.header("Uniform Distribution (Continuous)")
    st.markdown("Models events where all outcomes in an interval are equally likely.")
    render_formula(
        r"f(x) = \frac{1}{b - a}",
        {"a": "Minimum value", "b": "Maximum value (b > a)", "x": "Value (a $\le$ x $\le$ b)"}
    )
    
    with st.form("uniform_form"):
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("a (minimum)", value=0.0)
        with col2:
            b = st.number_input("b (maximum)", value=10.0)
        x = st.number_input("x (target value)", value=5.0)
        submit = st.form_submit_button("Calculate Distribution")
        
    if submit:
        if a >= b:
            st.error("Maximum (b) must be greater than minimum (a).")
        else:
            pdf, cdf = dist.calculate_uniform(a, b, x)
            st.success(f"**PDF at x={x}**: {format_number(pdf)}")
            st.info(f"**CDF ( P(X $\le$ {x}) )**: {format_number(cdf)}")
            
            df_plot = dist.generate_uniform_plot_data(a, b)
            fig = charts.plot_distribution_curve(df_plot, 'x', 'PDF', "Uniform PDF", is_discrete=False)
            st.plotly_chart(fig, use_container_width=True)
