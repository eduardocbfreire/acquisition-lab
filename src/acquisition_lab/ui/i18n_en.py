"""Interface strings in English. The only place with visible EN text."""

from __future__ import annotations

EN: dict[str, str] = {
    # App / header
    "app.title": "Acquisition Lab",
    "app.tab_error": "Unexpected error on the {name} tab. Reach out to Eduardo for a fix.",
    "app.tab_error_detail": "Technical detail",
    "app.caption": "Local acquisition analysis: funnel, cohort, media and sales. "
    "Every rate comes with a margin of uncertainty and the number of cases.",
    # Sidebar
    "sidebar.data_title": "Data",
    "sidebar.data_caption": "Upload your CSV files or use the example data. "
    "Everything runs on your machine.",
    "sidebar.use_example": "use example",
    "sidebar.upload_label": "{name} CSV",
    "sidebar.upload_help": "Expected header: {header}",
    "sidebar.rows_upload": "{n} rows loaded.",
    "sidebar.rows_example": "{n} rows (example).",
    "sidebar.err_csv": "Problem in the {name} CSV: {detail}",
    "sidebar.err_unexpected": "Unexpected error reading {name}: {detail}",
    "err.missing_column": "Could not find the '{col}' column in the {dataset} file. "
    "Check the header — the expected format is in the README.",
    "err.bad_dates": "The '{col}' column has values that are not dates (e.g. '{value}').",
    "err.not_numeric": "The '{col}' column has values that are not numbers (e.g. '{value}').",
    "err.empty_after_filters": "No rows are left with the current filters.",
    # Streamlit's built-in uploader text, translated via CSS
    "uploader.drag": "Drag and drop file here",
    "uploader.limit": "Limit 200 MB per file • CSV",
    "uploader.browse": "Browse files",
    # Dataset names
    "ds.funnel": "Funnel",
    "ds.cohort": "Cohort",
    "ds.media": "Media",
    "ds.sales": "Sales",
    # Tabs
    "tab.overview": "Overview",
    "tab.funnel": "Funnel",
    "tab.cohort": "Cohort",
    "tab.media": "Media",
    "tab.changepoints": "Change points",
    "tab.sales": "Sales",
    # Common
    "common.how_to_read": "How do I read this screen?",
    "common.learn_more": "Learn more",
    "common.ci_n": "95% interval [{lo}, {hi}] · n = {n} ({count} of {total})",
    "common.ci_n_simple": "95% interval [{lo}, {hi}] · n = {n}",
    "common.cac_disclaimer": "Descriptive CAC, not causal: it is computed from "
    "attributed conversions and is muddied by confounding (demand and seasonality "
    "move both spend and conversions together). Measuring true incremental impact "
    "needs a geo experiment or a synthetic control — beyond what a descriptive CSV "
    "analysis can do.",
    "common.missing_data": 'No {name} data yet. In the sidebar, tick "use example" '
    "or upload a CSV in the right format.",
    "common.spinner_cac": "Looking for change points in CAC…",
    # Overview
    "overview.caption": "The headline numbers from every screen, side by side. "
    "Each rate comes with its margin of uncertainty and the number of cases.",
    "overview.help": "This screen pulls everything into one place. Each card shows a "
    "number and, below it, the 95% interval — the range where the true value most "
    "likely sits. The narrower the range, the more you can trust the number. n is "
    "how many people or cases went into the math: if n is small, be skeptical.",
    "overview.no_data": 'No data loaded. Use the sidebar to tick "use example" or '
    "upload your CSVs. The project ships with example data.",
    "overview.funnel_label": "Funnel",
    "overview.metric.e2e": "End-to-end conversion",
    "overview.metric.e2e.help": "Out of every 100 people who came in, how many made "
    "it to the end. The interval shows the margin of uncertainty: the narrower, the "
    "more reliable.",
    "overview.retention_label": "Retention (period 1)",
    "overview.metric.retention": "Average retention, period 1",
    "overview.metric.retention.help": "Of the people who joined, what share came back "
    "in the next period, on average. Shown with its uncertainty interval.",
    "overview.retention_caption": "average of {n} mature cohorts",
    "overview.media_label": "Media (CAC)",
    "overview.metric.cac": "Cost per acquisition (CAC)",
    "overview.metric.cac.help": "How much was spent, on average, to land one "
    "acquisition. It is a picture of what happened, not proof that media caused the "
    "result.",
    "overview.cac_caption": "lag {lag}d · {n} change points",
    "overview.sales_label": "Sales (avg order value)",
    "overview.metric.aov": "Average order value",
    "overview.metric.aov.help": "How much each order is worth, on average. The "
    "interval is the margin of uncertainty around that average.",
    # Funnel
    "funnel.caption": "For each step, the share of people who move forward. It counts "
    "people (not events) and shows the margin of uncertainty next to each rate.",
    "funnel.help": "The funnel shows how many people move from one step to the next. "
    "Each bar is a step; conversion is how many carried on. The 95% interval is the "
    "margin of uncertainty, and n is how many people went into the math. People who "
    "arrived recently and have not had time to convert are left out, so they do not "
    "drag the rates down.",
    "funnel.steps_label": "Step order (entry → exit)",
    "funnel.steps_help": "The first step is the entry point; end-to-end rates use it "
    "as the base.",
    "funnel.maturation_label": "Waiting time (days)",
    "funnel.maturation_help": "People who joined more recently than this have not had "
    "time to convert and are left out of the math.",
    "funnel.min_steps_warn": "Pick at least 2 steps.",
    "funnel.excluded_info": "{n} people who joined in the last {days} days were left "
    "out: they have not had time to move forward yet.",
    "funnel.subheader_e2e": "From entry to the end",
    "funnel.e2e_caption": "Measured directly between entry and exit. You cannot just "
    "multiply the step rates: they are not independent.",
    "funnel.subheader_detail": "Step by step",
    "funnel.col.step": "step",
    "funnel.col.users": "people",
    "funnel.col.conv_prev": "conversion vs previous step",
    "funnel.col.ci_prev": "95% interval vs previous",
    "funnel.col.conv_e2e": "cumulative conversion",
    # Cohort
    "cohort.caption": "Groups people by when they joined and tracks how many come "
    "back over time. Each cell has a rate, the number of cases and a margin of "
    "uncertainty.",
    "cohort.help": "A cohort is a group of people who joined in the same period (by "
    "default, the same week). Each row is a cohort; each column is how much time has "
    "passed since they joined. The color shows the share still active. Groups that "
    "joined recently have fewer columns filled in — the blank cells have not "
    "happened yet, they are not zero.",
    "cohort.gran_label": "Group by",
    "cohort.gran.W": "Week",
    "cohort.gran.M": "Month",
    "cohort.periods_label": "Periods (0 to N)",
    "cohort.warn": "Do not compare cells of different ages: recent groups have less "
    "time observed. Blank cells have not been observed yet — they are not zero.",
    "cohort.sizes_subheader": "Size of each cohort",
    "cohort.col.cohort": "cohort",
    "cohort.col.size": "size",
    # Media
    "media.caption": "Cost per acquisition (CAC) week by week, with the delay between "
    "spending and converting already corrected, plus the points where cost shifted.",
    "media.help": "CAC is how much you spend to land each acquisition. Since "
    "conversions usually come a few days after the spend, we line the two up before "
    "dividing. The markers point to weeks where cost shifted to a new level. Note: "
    "this describes what happened, it does not prove media caused the result.",
    "media.auto_lag_label": "Find the delay automatically (suggested: {lag} days)",
    "media.manual_lag_label": "Manual delay (days)",
    "media.smooth_label": "Smoothing (weeks)",
    "media.metric.lag": "Delay used",
    "media.metric.lag.value": "{lag} days",
    "media.metric.lag.help": "How many days conversions typically lag the spend. We "
    "line the two up by this delay before computing cost.",
    "media.metric.cac": "Average CAC",
    "media.metric.cac.help": "Average cost per acquisition over the period. "
    "Descriptive: not proof of cause.",
    "media.metric.cps": "Change points",
    "media.metric.cps.help": "How many times cost per acquisition shifted to a new "
    "level in a consistent way.",
    "media.cps_found": "Weeks where cost shifted to a new level:",
    # Change points
    "cp.caption": "Automatically finds the moments when a series shifts in level, in "
    "spread or in trend.",
    "cp.help": "What it is for: finding WHEN a metric shifted to a new level — say, "
    "CAC stepping up after a certain week — automatically, without picking the date "
    "by eye. The method separates a real shift from ordinary ups and downs: it ignores "
    "small jumps and only keeps what holds up when the test tightens. Use the controls "
    "to make the search more or less sensitive.",
    "cp.no_data": "Load Media or Cohort data to get series to analyze.",
    "cp.series_label": "Series",
    "cp.series.spend": "Media · daily spend",
    "cp.series.conv": "Media · daily conversions",
    "cp.series.cac": "Media · weekly CAC",
    "cp.series.signups": "Cohort · new signups per day",
    "cp.cost_label": "What may have changed",
    "cp.cost.l2": "The level (mean)",
    "cp.cost.normal": "The spread",
    "cp.cost.linear": "The trend",
    "cp.cost_help": "l2 detects a change in mean level; normal, in variance; linear, " "in trend.",
    "cp.k_label": "Sensitivity",
    "cp.k_help": "Higher = fewer points, only the most obvious shifts. Start at 1.0 and "
    "raise it if noise creeps in.",
    "cp.minsize_label": "Minimum spacing between points",
    "cp.minsize_help": "Minimum number of points (days or weeks, depending on the "
    "series) between two changes. Keeps a short wobble from being marked as a change.",
    "cp.detrend_label": "Remove trend first",
    "cp.detrend_help": "When the series climbs or falls continuously (e.g. spend "
    "growing every month), the detector mistakes that slope for several level "
    "shifts. Removing the trend strips that background ramp and leaves only the real "
    "steps visible. Turn it on if the series has a clear long-term direction.",
    "cp.metric.cps": "Change points",
    "cp.metric.sigma": "Estimated noise",
    "cp.metric.sigma.help": "How much the series normally wiggles. It is the "
    "yardstick for deciding what counts as a real shift.",
    "cp.metric.pen": "Strictness (penalty)",
    "cp.metric.pen.help": "How much the series has to change to earn a new point. "
    "Higher = more conservative.",
    "cp.dropped_mag": "Skipped for a small jump: {n}",
    "cp.dropped_unstable": "Skipped for not holding up under a stricter test: {n}",
    "cp.min_points": "This dataset has {n} points; detection needs at least {min}.",
    "cp.spinner": "Looking for change points…",
    "cp.ref.ruptures": "Docs for **ruptures**, the library behind the detection — worth "
    "a look at its examples and parameters "
    "([ruptures-docs](https://centre-borelli.github.io/ruptures-docs/)).",
    "cp.ref.truong": "Truong, Oudre & Vayatis (2020), *Selective review of offline "
    "change point detection methods* — a friendly map of all the methods.",
    "cp.ref.killick": "Killick, Fearnhead & Eckley (2012) — the PELT paper, the exact "
    "algorithm running here under the hood.",
    # Sales
    "sales.caption": "Average order value (revenue divided by orders) with the margin "
    "of uncertainty done right, accounting for the fact that both move together.",
    "sales.help": "Average order value is total revenue divided by total orders. "
    "Since revenue and order count vary from person to person and move together, the "
    "margin of uncertainty has to account for that — otherwise it is wrong. "
    "Resampling (bootstrap) is an optional cross-check of the same number.",
    "sales.boot_label": "Cross-check by resampling (bootstrap, 10,000 times)",
    "sales.boot_help": "Redoes the math by drawing people at random with "
    "replacement, like a second opinion on the margin. Optional.",
    "sales.metric.aov": "Average order value (revenue / orders)",
    "sales.metric.aov.help": "How much each order is worth, on average. The 95% "
    "interval is the margin of uncertainty.",
    "sales.metric.se": "Full margin",
    "sales.metric.se.help": "Accounts for revenue and orders moving together (a "
    "technique known as the delta method).",
    "sales.metric.se_naive": "Simplified margin",
    "sales.metric.se_naive.help": "Treats the order count as fixed, ignoring that "
    "revenue and orders move together — shown for comparison.",
    "sales.info_cov_reduces": "Revenue and orders move together: people who order "
    "more spend more. Accounting for that makes the margin narrower than the naive "
    "way suggests. With other data it can go the other way — the point is not to "
    "treat the order count as fixed.",
    "sales.info_cov_generic": "The math accounts for revenue and orders moving "
    "together. Treating the order count as fixed gives the wrong margin.",
    "sales.boot_caption": "Resampling: {p}, 95% interval [{lo}, {hi}].",
    "sales.dist_caption": "The distribution is usually skewed (many low tickets, a few "
    "high ones) — that is why the average comes with an interval, not on its own.",
    "sales.boot_dist_caption": "If the two bands all but coincide, the delta method "
    "is validated.",
    "sales.sample_subheader": "A sample of the data",
    "sales.ref.delta": "Delta method for ratios: any *survey statistics* text on 'ratio "
    "estimators' explains why the denominator counts too.",
    "sales.ref.bootstrap": "Efron & Tibshirani, *An Introduction to the Bootstrap* — the "
    "classic read on the resampling method used in the cross-check.",
    # Charts (viz)
    "viz.funnel.title": "Funnel — {entered} entries counted " "({excluded} partial ones left out)",
    "viz.funnel.n": "n = {n}",
    "viz.funnel.conv_prev": "{rate} vs previous step",
    "viz.funnel.ci": "95% interval [{lo}, {hi}]",
    "viz.funnel.step_title": "Step-to-step conversion (95% interval)",
    "viz.funnel.step_yaxis": "conversion",
    "viz.cohort.title": "Retention by cohort (grouped by {gran})",
    "viz.cohort.xaxis": "periods since joining",
    "viz.cohort.yaxis": "cohort (when they joined)",
    "viz.cohort.hover": "cohort %{y} · period %{x}<br>retention %{z:.1%}<br>"
    "95% interval [%{customdata[0]:.1%}, %{customdata[1]:.1%}]<br>"
    "%{customdata[2]:.0f} of %{customdata[3]:.0f} people<extra></extra>",
    "viz.media.title": "Weekly CAC — {lag}-day delay",
    "viz.media.xaxis": "week",
    "viz.media.yaxis": "CAC (spend / acquisitions)",
    "viz.media.series_raw": "Weekly CAC",
    "viz.media.series_smooth": "Smoothed CAC",
    "viz.changepoint_marker": "change point",
    "viz.cp.xaxis": "period",
    "viz.cp.subtitle": "PELT/{model} · strictness={pen} · noise≈{sigma} · " "min spacing={min}",
    "viz.cp.disabled": "{message}",
    "viz.cp.segment_mean": "mean {mean}",
    "viz.sales.title": "Average order value = {ratio} · 95% interval by method",
    "viz.sales.compare_xaxis": "average order value (R$)",
    "viz.sales.compare_hover": "AOV {ratio} · margin ±{half}",
    "viz.sales.method.delta": "Full margin",
    "viz.sales.method.naive": "Simplified margin",
    "viz.sales.dist.title": "Per-user order value distribution",
    "viz.sales.dist.xaxis": "order value per user (R$)",
    "viz.sales.dist.yaxis": "users",
    "viz.sales.dist.aov_line": "average",
    "viz.sales.boot.title": "Distribution of resampled estimates",
    "viz.sales.boot.xaxis": "resampled average order value (R$)",
    "viz.sales.boot.yaxis": "resamples",
    "viz.sales.boot.band": "95% CI (bootstrap)",
    "viz.sales.boot.delta": "95% CI (delta method)",
}
