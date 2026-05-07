from pathlib import Path

from streamlit.testing.v1 import AppTest

from data.diseases import DISEASE_DETAILS


APP_PATH = Path(__file__).resolve().parents[2] / "app.py"


def _load_diagnosis_page() -> AppTest:
    app = AppTest.from_file(str(APP_PATH))
    app.run()
    app.radio[0].set_value("Diagnosis").run()
    return app


def _slider_map(app: AppTest) -> dict[str, object]:
    return {slider.key: slider for slider in app.slider}


def test_diagnosis_requires_at_least_one_symptom() -> None:
    app = _load_diagnosis_page()

    app.button[1].click().run()

    assert len(app.warning) == 1
    assert app.warning[0].value == "Pilih minimal satu gejala sebelum menjalankan diagnosis."
    assert len(app.metric) == 0


def test_diagnosis_flow_ranks_anthracnose_first() -> None:
    app = _load_diagnosis_page()
    sliders = _slider_map(app)

    sliders["slider_G01"].set_value(1.0)
    sliders["slider_G02"].set_value(0.8)
    sliders["slider_G03"].set_value(0.9)
    sliders["slider_G25"].set_value(0.7)

    app.button[1].click().run()

    metrics = {metric.label: metric.value for metric in app.metric}
    assert metrics["Penyakit Utama"] == "Antraknosa (Busuk Buah)"
    assert metrics["Kode"] == "P1"
    assert metrics["Certainty Factor"] == "0.9970"
    assert metrics["Tingkat Kepercayaan"] == "99.70%"

    assert app.success[0].value == "Interpretasi hasil utama: **Sangat Kuat**"

    ranking_df = app.dataframe[0].value
    assert ranking_df.iloc[0]["Kode"] == "P1"
    assert ranking_df.iloc[0]["Penyakit"] == "Antraknosa (Busuk Buah)"
    assert ranking_df.iloc[0]["Interpretasi"] == "Sangat Kuat"

    history_df = app.dataframe[2].value
    assert history_df.iloc[0]["Penyakit Utama"] == "Antraknosa (Busuk Buah)"
    assert history_df.iloc[0]["Persentase"] == 99.7


def test_reset_form_clears_sliders_and_hides_previous_results() -> None:
    app = _load_diagnosis_page()
    sliders = _slider_map(app)

    sliders["slider_G18"].set_value(1.0)
    sliders["slider_G19"].set_value(0.8)
    sliders["slider_G20"].set_value(0.7)
    app.button[1].click().run()

    assert any(metric.value == "P6" for metric in app.metric)

    app.button[0].click().run()

    assert all(slider.value == 0.0 for slider in app.slider)
    assert len(app.metric) == 0


def test_home_page_renders_metrics_and_guidance() -> None:
    app = AppTest.from_file(str(APP_PATH))
    app.run()

    metrics = {metric.label: metric.value for metric in app.metric}
    assert metrics == {
        "Jumlah Penyakit": "7",
        "Jumlah Gejala": "25",
        "Output": "Excel .xlsx",
    }
    assert "Gunakan menu `Diagnosis`" in app.info[0].value


def test_info_penyakit_page_lists_all_diseases() -> None:
    app = AppTest.from_file(str(APP_PATH))
    app.run()
    app.radio[0].set_value("Info Penyakit").run()

    expander_labels = [expander.label for expander in app.expander]
    expected = [f"{code} - {detail['name']}" for code, detail in DISEASE_DETAILS.items()]
    assert expander_labels == expected
    assert app.caption[0].value.startswith("Ringkasan penyakit utama")


def test_about_page_shows_method_and_disclaimer() -> None:
    app = AppTest.from_file(str(APP_PATH))
    app.run()
    app.radio[0].set_value("Tentang Metode").run()

    assert app.title[0].value == "Tentang Metode"
    markdown_values = "\n".join(markdown.value for markdown in app.markdown)
    assert "Forward Chaining" in markdown_values
    assert "CF(H,E) = CF_Pakar x CF_User" in markdown_values
    assert "hasil tidak menggantikan" in app.warning[0].value.lower()
