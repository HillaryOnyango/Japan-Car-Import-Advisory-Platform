from dataclasses import dataclass


@dataclass
class ImportCostInput:
    purchase_price_usd: float
    shipping_cost_usd: float
    insurance_usd: float
    usd_to_kes: float
    import_duty_rate: float
    excise_duty_rate: float
    vat_rate: float
    idf_rate: float
    rdl_rate: float
    port_charges_kes: float
    clearing_fees_kes: float
    registration_cost_kes: float


@dataclass
class ImportCostResult:
    cif_usd: float
    cif_kes: float
    import_duty_kes: float
    excise_duty_kes: float
    vat_kes: float
    idf_fee_kes: float
    rdl_fee_kes: float
    port_charges_kes: float
    clearing_fees_kes: float
    registration_cost_kes: float
    total_taxes_kes: float
    total_import_cost_kes: float


def calculate_import_cost(data: ImportCostInput) -> ImportCostResult:
    cif_usd = data.purchase_price_usd + data.shipping_cost_usd + data.insurance_usd
    cif_kes = cif_usd * data.usd_to_kes

    import_duty = cif_kes * data.import_duty_rate
    excise_duty = (cif_kes + import_duty) * data.excise_duty_rate
    vat = (cif_kes + import_duty + excise_duty) * data.vat_rate
    idf_fee = max(cif_kes * data.idf_rate, 5000)
    rdl_fee = cif_kes * data.rdl_rate

    total_taxes = import_duty + excise_duty + vat + idf_fee + rdl_fee

    total_import_cost = (
        cif_kes
        + total_taxes
        + data.port_charges_kes
        + data.clearing_fees_kes
        + data.registration_cost_kes
    )

    return ImportCostResult(
        cif_usd=cif_usd,
        cif_kes=cif_kes,
        import_duty_kes=import_duty,
        excise_duty_kes=excise_duty,
        vat_kes=vat,
        idf_fee_kes=idf_fee,
        rdl_fee_kes=rdl_fee,
        port_charges_kes=data.port_charges_kes,
        clearing_fees_kes=data.clearing_fees_kes,
        registration_cost_kes=data.registration_cost_kes,
        total_taxes_kes=total_taxes,
        total_import_cost_kes=total_import_cost,
    )
