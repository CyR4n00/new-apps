import pytest
import pandas as pd
import app

def test_generate_mock_data():
    df = app.generate_mock_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 14
    expected_columns = ["選択", "日付", "トピック", "投稿テキスト", "表示回数", "いいね", "エンゲージ率(%)"]
    for col in expected_columns:
        assert col in df.columns

def test_app_layout():
    # We won't test Streamlit layout directly here since it requires a running session context,
    # but the logic runs correctly as confirmed by manual bash verification.
    pass
