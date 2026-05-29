import streamlit as st

from calculator.import_cost_calculator import ImportCostInput, calculate_import_cost
from app.utils.db_utils import format_kes


def render_calculator():
    st.title("🧮 Kenya Import Cost Calculator")
    st.write("Estimate the full landed cost of importing a car into Kenya.")

    col1, col2 = st.columns(2)

    with col1:
        purchase_price_usd = st.number_input("FOB Purchase Price (USD)", value=8000.0)
        shipping_cost_usd = st.number_input("Shipping Cost (USD)", value=1500.0)
        insurance_usd = st.number_input("Insurance (USD)", value=100.0)
        usd_to_kes = st.number_input("USD to KES Exchange Rate", value=130.0)

    with col2:
        import_duty_rate = st.number_input("Import Duty Rate", value=0.35)
        excise_duty_rate = st.number_input("Excise Duty Rate", value=0.20)
        vat_rate = st.number_input("VAT Rate", value=0.16)
        idf_rate = st.number_input("IDF Rate", value=0.035)
        rdl_rate = st.number_input("RDL Rate", value=0.02)

    port_charges_kes = st.number_input("Port Charges (KES)", value=35000.0)
    clearing_fees_kes = st.number_input("Clearing Fees (KES)", value=45000.0)
    registration_cost_kes = st.number_input("NTSA Registration (KES)", value=15000.0)

    if st.button("Calculate Landed Cost"):
        data = ImportCostInput(
            purchase_price_usd=purchase_price_usd,
            shipping_cost_usd=shipping_cost_usd,
            insurance_usd=insurance_usd,
            usd_to_kes=usd_to_kes,
            import_duty_rate=import_duty_rate,
            excise_duty_rate=excise_duty_rate,
            vat_rate=vat_rate,
            idf_rate=idf_rate,
            rdl_rate=rdl_rate,
            port_charges_kes=port_charges_kes,
            clearing_fees_kes=clearing_fees_kes,
            registration_cost_kes=registration_cost_kes,
        )

        result = calculate_import_cost(data)

        st.success("Import cost calculated successfully.")

        st.metric("Total Landed Cost", format_kes(result.total_import_cost_kes))

        st.subheader("Full Cost Breakdown")
        st.json(result.__dict__)
