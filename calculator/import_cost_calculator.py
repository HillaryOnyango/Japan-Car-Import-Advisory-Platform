from dataclasses import dataclass

@dataclass
class ImportCostInput:
    purchase_price_usd: float
    shipping_cost_usd: float
    exchange_rate: float
    insurance_rate: float = 0.015
    import_duty_rate: float = 0.25
    excise_duty_rate: float = 0.20
    vat_rate: float = 0.16
    idf_rate: float = 0.025
    rdl_rate: float = 0.02
    port_charges_kes: float = 50000
    clearing_fees_kes: float = 70000
    registration_cost_kes: float = 13800
    other_charges_kes: float = 30000


def calculate_import_cost(data: ImportCostInput) -> dict:
    purchase_kes = data.purchase_price_usd * data.exchange_rate
    shipping_kes = data.shipping_cost_usd * data.exchange_rate
    insurance_kes = purchase_kes * data.insurance_rate

    cif_kes = purchase_kes + shipping_kes + insurance_kes
    import_duty = cif_kes * data.import_duty_rate
    excise_duty = (cif_kes + import_duty) * data.excise_duty_rate
    vat = (cif_kes + import_duty + excise_duty) * data.vat_rate
    idf = cif_kes * data.idf_rate
    rdl = cif_kes * data.rdl_rate

    total_taxes = import_duty + excise_duty + vat + idf + rdl
    total_landed_cost = (
        cif_kes + total_taxes + data.port_charges_kes + data.clearing_fees_kes
        + data.registration_cost_kes + data.other_charges_kes
    )

    return {
        "purchase_kes": purchase_kes,
        "shipping_kes": shipping_kes,
        "insurance_kes": insurance_kes,
        "cif_kes": cif_kes,
        "import_duty": import_duty,
        "excise_duty": excise_duty,
        "vat": vat,
        "idf": idf,
        "rdl": rdl,
        "total_taxes": total_taxes,
        "port_charges_kes": data.port_charges_kes,
        "clearing_fees_kes": data.clearing_fees_kes,
        "registration_cost_kes": data.registration_cost_kes,
        "other_charges_kes": data.other_charges_kes,
        "total_landed_cost_kes": total_landed_cost,
    }
