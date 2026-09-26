import streamlit as st
import pandas as pd
import math

# ============================ НАСТРОЙКИ ============================

FONT_SIZE_TABLE = 18
DECIMALS = 2

# ============================ КОНСТАНТЫ ============================

CLIMATE_SCALE = [
    "Арктический", "Умеренно-холодный", "Умеренный",
    "Субтропический", "Средиземноморский", "Тропический", "Пустынный",
]

COUNTRY_CLIMATE = {
    "Россия": 1, "Германия": 2, "Испания": 4, "Италия": 4, "Португалия": 4,
    "Франция": 3, "Великобритания": 2, "Норвегия": 0, "Швеция": 0,
    "Финляндия": 0, "Швейцария": 1, "Польша": 2, "Чехия": 2,
    "Сербия": 3, "Черногория": 3, "Кипр": 4,
    "Греция": 4, "Мальта": 4, "Хорватия": 3, "Албания": 4,
    "Украина": 2, "Беларусь": 2, "Румыния": 3, "Болгария": 3,
    "Латвия": 1, "Литва": 1, "Словения": 3, "Словакия": 2,
    "США": 3, "Канада": 1, "Мексика": 4, "Аргентина": 3, "Бразилия": 5,
    "Чили": 4, "Перу": 5,
    "Таиланд": 5, "Вьетнам": 5, "ОАЭ": 6, "Турция": 3,
    "Грузия": 3, "Армения": 2, "Казахстан": 1, "Китай": 3, "Япония": 3,
    "Индия": 5, "Индонезия": 5, "Малайзия": 5, "Южная Корея": 3,
    "Узбекистан": 1, "Саудовская Аравия": 6,
    "Египет": 6, "Марокко": 4, "Тунис": 4, "ЮАР": 4,
    "Австралия": 4, "Новая Зеландия": 3,
}

CRIME_INDEX = {
    "Россия": 40, "Германия": 32, "Испания": 30, "Италия": 45, "Португалия": 23,
    "Франция": 48, "Великобритания": 45, "США": 47, "Канада": 32, "Мексика": 65,
    "Аргентина": 60, "Бразилия": 68, "Таиланд": 38, "Вьетнам": 35, "ОАЭ": 15,
    "Египет": 55, "Турция": 35, "Грузия": 30, "Армения": 25, "Казахстан": 35,
    "Китай": 30, "Япония": 22, "Австралия": 35, "Новая Зеландия": 30,
    "Норвегия": 28, "Швеция": 42, "Финляндия": 25, "Швейцария": 22,
    "Польша": 25, "Чехия": 20, "Сербия": 35, "Черногория": 30, "Кипр": 25,
    "Израиль": 40, "Индия": 45, "Индонезия": 40,
    "Греция": 46.4, "Мальта": 43.0, "Хорватия": 25.5, "Албания": 44.7,
    "Украина": 47.0, "Беларусь": 49.8, "Румыния": 32.3, "Болгария": 36.1,
    "Чили": 60.5, "Перу": 67.1, "Марокко": 47.8, "Тунис": 45.1,
    "Саудовская Аравия": 23.9, "Малайзия": 48.9, "Южная Корея": 24.9,
    "Узбекистан": 27.9, "Латвия": 37.1, "Литва": 32.4,
    "Словения": 23.8, "Словакия": 31.0, "ЮАР": 74.7,
}

GPI_SCORE = {
    "Россия": 3.15, "Германия": 1.45, "Испания": 1.65, "Италия": 1.75,
    "Португалия": 1.35, "Франция": 1.80, "Великобритания": 1.65, "США": 2.45,
    "Канада": 1.35, "Мексика": 2.60, "Аргентина": 1.85, "Бразилия": 2.10,
    "Таиланд": 2.00, "Вьетнам": 1.75, "ОАЭ": 1.60, "Египет": 2.30,
    "Турция": 2.60, "Грузия": 1.85, "Армения": 1.95, "Казахстан": 1.95,
    "Китай": 2.10, "Япония": 1.35, "Австралия": 1.55, "Новая Зеландия": 1.30,
    "Норвегия": 1.35, "Швеция": 1.55, "Финляндия": 1.30, "Швейцария": 1.35,
    "Польша": 1.65, "Чехия": 1.35, "Сербия": 1.85, "Черногория": 1.80,
    "Кипр": 1.80, "Израиль": 2.75, "Индия": 2.30, "Индонезия": 1.80,
    "Греция": 1.76, "Мальта": 1.65, "Хорватия": 1.52, "Албания": 1.81,
    "Украина": 3.40, "Беларусь": 2.50, "Румыния": 1.72, "Болгария": 1.61,
    "Чили": 1.80, "Перу": 2.10, "Марокко": 2.05, "Тунис": 2.10,
    "Саудовская Аравия": 2.05, "Малайзия": 1.47, "Южная Корея": 1.80,
    "Узбекистан": 2.10, "Латвия": 1.56, "Литва": 1.56,
    "Словения": 1.41, "Словакия": 1.61, "ЮАР": 2.30,
}

PURCHASING_POWER = {
    "Россия": 40, "Германия": 100, "Испания": 70, "Италия": 65, "Португалия": 55,
    "Франция": 80, "Великобритания": 85, "США": 105, "Канада": 85, "Мексика": 45,
    "Аргентина": 35, "Бразилия": 35, "Таиланд": 40, "Вьетнам": 35, "ОАЭ": 95,
    "Египет": 25, "Турция": 40, "Грузия": 35, "Армения": 35, "Казахстан": 40,
    "Китай": 60, "Япония": 80, "Австралия": 95, "Новая Зеландия": 85,
    "Норвегия": 100, "Швеция": 95, "Финляндия": 90, "Швейцария": 130,
    "Польша": 55, "Чехия": 60, "Сербия": 40, "Черногория": 40, "Кипр": 65,
    "Израиль": 85, "Индия": 30, "Индонезия": 30,
    "Греция": 62.3, "Мальта": 76.6, "Хорватия": 82.0, "Албания": 46.9,
    "Украина": 35.0, "Беларусь": 63.7, "Румыния": 72.7, "Болгария": 78.6,
    "Чили": 50.4, "Перу": 48.4, "Марокко": 43.7, "Тунис": 42.0,
    "Саудовская Аравия": 115.7, "Малайзия": 76.3, "Южная Корея": 101.7,
    "Узбекистан": 40.0, "Латвия": 74.1, "Литва": 87.5,
    "Словения": 87.0, "Словакия": 73.4, "ЮАР": 105.5,
}

ISO3 = {
    "Россия": "RUS", "Германия": "DEU", "Испания": "ESP", "Италия": "ITA",
    "Португалия": "PRT", "Франция": "FRA", "Великобритания": "GBR", "США": "USA",
    "Канада": "CAN", "Мексика": "MEX", "Аргентина": "ARG", "Бразилия": "BRA",
    "Таиланд": "THA", "Вьетнам": "VNM", "ОАЭ": "ARE", "Египет": "EGY",
    "Турция": "TUR", "Грузия": "GEO", "Армения": "ARM", "Казахстан": "KAZ",
    "Китай": "CHN", "Япония": "JPN", "Австралия": "AUS", "Новая Зеландия": "NZL",
    "Норвегия": "NOR", "Швеция": "SWE", "Финляндия": "FIN", "Швейцария": "CHE",
    "Польша": "POL", "Чехия": "CZE", "Сербия": "SRB", "Черногория": "MNE",
    "Кипр": "CYP", "Израиль": "ISR", "Индия": "IND", "Индонезия": "IDN",
    "Греция": "GRC", "Мальта": "MLT", "Хорватия": "HRV", "Албания": "ALB",
    "Украина": "UKR", "Беларусь": "BLR", "Румыния": "ROU", "Болгария": "BGR",
    "Чили": "CHL", "Перу": "PER", "Марокко": "MAR", "Тунис": "TUN",
    "Саудовская Аравия": "SAU", "Малайзия": "MYS", "Южная Корея": "KOR",
    "Узбекистан": "UZB", "Латвия": "LVA", "Литва": "LTU",
    "Словения": "SVN", "Словакия": "SVK", "ЮАР": "ZAF",
}

def _flag(iso2: str) -> str:
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in iso2.upper())

FLAGS = {
    "Россия": _flag("RU"), "Германия": _flag("DE"), "Испания": _flag("ES"),
    "Италия": _flag("IT"), "Португалия": _flag("PT"), "Франция": _flag("FR"),
    "Великобритания": _flag("GB"), "США": _flag("US"), "Канада": _flag("CA"),
    "Мексика": _flag("MX"), "Аргентина": _flag("AR"), "Бразилия": _flag("BR"),
    "Таиланд": _flag("TH"), "Вьетнам": _flag("VN"), "ОАЭ": _flag("AE"),
    "Египет": _flag("EG"), "Турция": _flag("TR"), "Грузия": _flag("GE"),
    "Армения": _flag("AM"), "Казахстан": _flag("KZ"), "Китай": _flag("CN"),
    "Япония": _flag("JP"), "Австралия": _flag("AU"),
    "Новая Зеландия": _flag("NZ"), "Норвегия": _flag("NO"),
    "Швеция": _flag("SE"), "Финляндия": _flag("FI"),
    "Швейцария": _flag("CH"), "Польша": _flag("PL"), "Чехия": _flag("CZ"),
    "Сербия": _flag("RS"), "Черногория": _flag("ME"), "Кипр": _flag("CY"),
    "Израиль": _flag("IL"), "Индия": _flag("IN"), "Индонезия": _flag("ID"),
    "Греция": _flag("GR"), "Мальта": _flag("MT"), "Хорватия": _flag("HR"),
    "Албания": _flag("AL"), "Украина": _flag("UA"), "Беларусь": _flag("BY"),
    "Румыния": _flag("RO"), "Болгария": _flag("BG"), "Чили": _flag("CL"),
    "Перу": _flag("PE"), "Марокко": _flag("MA"), "Тунис": _flag("TN"),
    "Саудовская Аравия": _flag("SA"), "Малайзия": _flag("MY"),
    "Южная Корея": _flag("KR"), "Узбекистан": _flag("UZ"),
    "Латвия": _flag("LV"), "Литва": _flag("LT"), "Словения": _flag("SI"),
    "Словакия": _flag("SK"), "ЮАР": _flag("ZA"),
}

# Запасные значения зарплаты / ВВП на душу (USD/год), если World Bank молчит.
SALARY_FALLBACK = {
    "Хорватия": 22000, "Греция": 23000, "Мальта": 37000, "Албания": 8500,
    "Украина": 5200, "Беларусь": 7900, "Румыния": 18500, "Болгария": 15800,
    "Чили": 17000, "Перу": 7900, "Марокко": 3700, "Тунис": 3900,
    "Саудовская Аравия": 32000, "Малайзия": 13000, "Южная Корея": 35000,
    "Узбекистан": 2500, "Латвия": 23000, "Литва": 28000,
    "Словения": 32000, "Словакия": 24000, "ЮАР": 6200,
    "Сербия": 12000, "Черногория": 12000, "Турция": 13000,
    "Грузия": 8100, "Армения": 8500, "Казахстан": 13500,
    "Таиланд": 7300, "Вьетнам": 4300, "Египет": 3500,
    "Индия": 2700, "Индонезия": 5100,
}

DEBT_FALLBACK = {
    "Сербия": 48, "Черногория": 65, "Россия": 20, "Казахстан": 25,
    "Армения": 48, "Грузия": 40, "Турция": 30, "Египет": 95,
    "Аргентина": 90, "Бразилия": 85, "Мексика": 55, "Таиланд": 62,
    "Вьетнам": 37, "Израиль": 62, "Кипр": 75, "Индия": 82,
    "Индонезия": 40, "Китай": 84, "ЮАР": 75, "Польша": 50,
    "Чехия": 44, "Венгрия": 74, "Румыния": 52, "Болгария": 23,
    "Хорватия": 63, "Словения": 68, "Словакия": 58, "Литва": 38,
    "Латвия": 44, "Эстония": 22, "Украина": 85, "Молдова": 35,
    "Беларусь": 40, "Узбекистан": 35, "Азербайджан": 18,
    "Греция": 150.9, "Мальта": 47.4, "Албания": 55.7,
    "Чили": 40.0, "Перу": 30.0, "Марокко": 70.0, "Тунис": 80.0,
    "Саудовская Аравия": 30.0, "Малайзия": 65.0, "Южная Корея": 55.0,
}

# ============================ ФУНКЦИИ ============================

def norm_inverse(v, vmin, vmax):
    if v is None: return 5.0
    if v <= vmin: return 10.0
    if v >= vmax: return 1.0
    return 10.0 - (v - vmin) / (vmax - vmin) * 9.0

def norm_direct(v, vmin, vmax):
    if v is None: return 5.0
    if v <= vmin: return 1.0
    if v >= vmax: return 10.0
    return 1.0 + (v - vmin) / (vmax - vmin) * 9.0


def sanitize_number(val, min_val=None, max_val=None, default=None):
    if val is None:
        return default
    try:
        v = float(val)
    except (TypeError, ValueError, OverflowError):
        return default
    if math.isnan(v) or math.isinf(v):
        return default
    if min_val is not None and v < min_val:
        return min_val
    if max_val is not None and v > max_val:
        return max_val
    return v


def round_to(value, decimals=DECIMALS):
    if value is None:
        return None
    return round(float(value), decimals)


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_wb(iso3, indicator):
    try:
        import requests
        url = (f"https://api.worldbank.org/v2/country/{iso3}"
               f"/indicator/{indicator}?format=json&mrnev=1")
        r = requests.get(url, timeout=10)
        data = r.json()
        if len(data) > 1 and data[1]:
            v = data[1][0].get("value")
            return v
    except Exception:
        return None
    return None


def calculate(country, climate_idx, weights, overrides=None):
    overrides = overrides or {}

    crime = CRIME_INDEX.get(country)
    gpi   = GPI_SCORE.get(country)
    pp    = PURCHASING_POWER.get(country)

    iso3 = ISO3.get(country)
    salary    = overrides.get("salary")
    inflation = overrides.get("inflation")
    debt      = overrides.get("debt")

    if salary is None and iso3:
        salary = fetch_wb(iso3, "NY.GDP.PCAP.CD")
        if salary is None and country in SALARY_FALLBACK:
            salary = SALARY_FALLBACK[country]

    if inflation is None and iso3:
        inflation = fetch_wb(iso3, "FP.CPI.TOTL.ZG")

    if debt is None and iso3:
        debt = fetch_wb(iso3, "GC.DOD.TOTL.GD.ZS")
        if debt is None and country in DEBT_FALLBACK:
            debt = DEBT_FALLBACK[country]

    scores = {}
    scores["safety"] = norm_inverse(crime, 15, 70)
    scores["peace"]  = norm_inverse(gpi, 1.2, 3.3)

    c_clim = COUNTRY_CLIMATE.get(country, 2)
    scores["climate"] = max(1.0, 10.0 - abs(climate_idx - c_clim))

    scores["salary"] = norm_direct(salary, 2000, 60000)

    inf_s  = norm_inverse(abs(inflation), 0, 20) if inflation is not None else 5.0
    debt_s = norm_inverse(debt, 0, 150)           if debt      is not None else 5.0
    scores["economy"] = (inf_s + debt_s) / 2

    scores["purchasing"] = norm_direct(pp, 20, 120)

    total = 0.0
    max_possible = 0.0
    for key in scores:
        w = weights[key]
        total += w * scores[key]
        max_possible += w * 10

    values = {
        "crime": crime, "gpi": gpi, "salary": salary,
        "inflation": inflation, "debt": debt,
        "purchasing": pp, "climate_idx": c_clim,
    }
    return total, max_possible, scores, values


# ============================ ИНТЕРФЕЙС ============================

st.set_page_config(
    page_title="Калькулятор страны проживания",
    page_icon="🌍",
    layout="wide",
)

st.markdown(f"""
<style>
[data-testid="stTable"] table {{
    font-size: {FONT_SIZE_TABLE}px !important;
}}
[data-testid="stTable"] th {{
    font-size: {FONT_SIZE_TABLE}px !important;
    font-weight: 700 !important;
}}
[data-testid="stTable"] td {{
    font-size: {FONT_SIZE_TABLE}px !important;
}}
[data-testid="stDataFrame"] {{
    font-size: {FONT_SIZE_TABLE}px !important;
}}
</style>
""", unsafe_allow_html=True)

st.title("🌍 Калькулятор страны проживания")
st.caption("Выберите страну, настройте важность критериев и сравните результаты.")

st.header("ШАГ 1 — Выбор страны")

country_list = sorted(COUNTRY_CLIMATE.keys())
country = st.selectbox(
    "Страна:",
    country_list,
    index=country_list.index("Португалия"),
)

st.header("ШАГ 2 — Климат и веса критериев")

climate_choice = st.radio(
    "Желаемый климат:",
    options=CLIMATE_SCALE,
    index=4,
    horizontal=True,
)
climate_idx = CLIMATE_SCALE.index(climate_choice)

st.subheader("Важность критериев")
col1, col2 = st.columns(2)
with col1:
    w_safety     = st.slider("Безопасность (Crime Index)", 1, 10, 5)
    w_peace      = st.slider("Мир (GPI)", 1, 10, 5)
    w_climate    = st.slider("Климат", 1, 10, 5)
with col2:
    w_salary     = st.slider("Средняя зарплата / ВВП", 1, 10, 5)
    w_economy    = st.slider("Экономика (инфляция / госдолг)", 1, 10, 5)
    w_purchasing = st.slider("Покупательная способность", 1, 10, 5)

weights = {
    "safety": w_safety, "peace": w_peace, "climate": w_climate,
    "salary": w_salary, "economy": w_economy, "purchasing": w_purchasing,
}

with st.expander("✏ Ручная корректировка значений (если нужно)"):
    st.caption(
        "Поля принимают только числа в допустимых пределах. "
        "Оставьте пустыми, чтобы использовать данные автоматически."
    )
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        ov_salary = st.number_input(
            "Зарплата / ВВП, USD/год",
            min_value=0.0, max_value=1_000_000.0,
            value=None, step=1000.0, format="%.0f",
            key="ov_salary",
        )
    with cc2:
        ov_infl = st.number_input(
            "Инфляция, %",
            min_value=-50.0, max_value=500.0,
            value=None, step=0.1, format="%.1f",
            key="ov_infl",
        )
    with cc3:
        ov_debt = st.number_input(
            "Госдолг, % ВВП",
            min_value=0.0, max_value=1000.0,
            value=None, step=1.0, format="%.0f",
            key="ov_debt",
        )

overrides = {}
s = sanitize_number(ov_salary, min_val=0.0, max_val=1_000_000.0)
if s is not None:
    overrides["salary"] = s
i = sanitize_number(ov_infl, min_val=-50.0, max_val=500.0)
if i is not None:
    overrides["inflation"] = i
d = sanitize_number(ov_debt, min_val=0.0, max_val=1000.0)
if d is not None:
    overrides["debt"] = d

with st.spinner("Загрузка данных..."):
    total, max_possible, scores, values = calculate(
        country, climate_idx, weights, overrides)

percent = (total / max_possible * 100) if max_possible else 0

st.header("Результат")

colA, colB, colC = st.columns(3)
colA.metric("ИТОГО", f"{total:.2f} / {max_possible:.0f}")
colB.metric("% совпадения", f"{percent:.2f}%")
colC.metric("Страна", f"{FLAGS.get(country, '')} {country}")

criteria_labels = {
    "safety":     "Безопасность (Crime Index)",
    "peace":      "Мир (GPI)",
    "climate":    "Климат",
    "salary":     "Средняя зарплата / ВВП на чел.",
    "economy":    "Экономика: инфляция / госдолг",
    "purchasing": "Покупательная способность",
}
values_display = {
    "safety":     f"{values['crime']:.0f}" if values['crime'] is not None else "—",
    "peace":      f"{values['gpi']:.2f}"   if values['gpi']   is not None else "—",
    "climate":    CLIMATE_SCALE[values['climate_idx']],
    "salary":     f"{values['salary']:.0f} USD/год" if values['salary'] else "—",
    "economy":    (f"{values['inflation']:.1f}% / {values['debt']:.0f}% ВВП"
                   if values['inflation'] is not None and values['debt'] is not None
                   else ("? / " + (f"{values['debt']:.0f}% ВВП"
                                   if values['debt'] is not None else "? ВВП"))),
    "purchasing": f"{values['purchasing']:.0f}" if values['purchasing'] is not None else "—",
}

criteria_rows = []
for key in ["safety", "peace", "climate", "salary", "economy", "purchasing"]:
    criteria_rows.append({
        "Критерий": criteria_labels[key],
        "Значение": values_display[key],
        "Вес": weights[key],
        "Балл": round_to(scores[key]),
        "Вклад": round_to(scores[key] * weights[key]),
    })

df = pd.DataFrame(criteria_rows)
st.table(df)

if "comparison" not in st.session_state:
    st.session_state.comparison = []

st.header("Сравнение стран")

btn_col1, btn_col2 = st.columns([1, 1])
with btn_col1:
    if st.button("➕ Добавить в сравнение", use_container_width=True):
        flag = FLAGS.get(country, "")
        rounded = round_to(percent)
        updated = False
        for row in st.session_state.comparison:
            if row["Страна"] == country:
                row.update({
                    "Флаг": flag,
                    "% совпадения": rounded,
                    "_raw_pct": percent,
                })
                updated = True
                break
        if not updated:
            st.session_state.comparison.append({
                "Флаг": flag,
                "Страна": country,
                "% совпадения": rounded,
                "_raw_pct": percent,
            })
        st.rerun()

with btn_col2:
    if st.button("🧹 Очистить сравнение", use_container_width=True):
        st.session_state.comparison = []
        st.rerun()

if st.session_state.comparison:
    sorted_pcts = sorted(
        {r["_raw_pct"] for r in st.session_state.comparison}, reverse=True)
    top2 = set(sorted_pcts[:2])

    cmp_df = pd.DataFrame(st.session_state.comparison)
    cmp_display = cmp_df[["Флаг", "Страна", "% совпадения"]].copy()

    def highlight_row(row):
        raw = cmp_df.loc[row.name, "_raw_pct"]
        if raw in top2:
            return ["background-color: #E8F5E9; color: #1B4332; font-weight: bold"] * 3
        return [""] * 3

    styled = cmp_display.style.apply(highlight_row, axis=1)
    st.table(styled)
else:
    st.info("Пока пусто. Нажмите «➕ Добавить в сравнение», чтобы добавить страну.")

st.divider()
st.caption(
    "Данные: World Bank (зарплата, инфляция, госдолг), "
    "Numbeo/GPI/IEP (безопасность, мир, покупательная способность). "
    "Показатели климата, экономики и части госдолга — из справочника."
)