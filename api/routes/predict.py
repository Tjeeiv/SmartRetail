from fastapi import APIRouter
from api.models.schemas import SalesInput, SalesOutput
from Services.mlservice import predictrevenue

router = APIRouter()

@router.post("/predict-sales", response_model=SalesOutput)
def predict_sales(input: SalesInput):
    features = {
        "MonthlyRevenue": input.MonthlyRevenue,
        "Invoicecount": input.Invoicecount,
        "monAvgRev": input.monAvgRev    
    }

    for m in range(1, 13):
        features[f"month_{m}"] = 1 if input.monthnumber == m else 0
    predicted = predictrevenue(features)
    return SalesOutput(predictedrevenue=predicted)
 