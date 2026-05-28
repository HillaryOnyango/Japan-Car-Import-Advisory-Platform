from calculator.import_cost_calculator import ImportCostInput, calculate_import_cost


def test_calculate_import_cost_returns_total():
    data = ImportCostInput(
        purchase_price_usd=8000,
        shipping_cost_usd=1200,
        exchange_rate=130,
    )
    result = calculate_import_cost(data)
    assert "total_landed_cost_kes" in result
    assert result["total_landed_cost_kes"] > 0
