import os
import yaml
from pathlib import Path

def write_artifacts(run_name, forecast, model, prediction_job, backtest_specs):
    """Write timeseries to csv and generate PDF of result"""
    
    # Create output dir
    outdir = Path(f'output/{run_name}')
    if not os.path.exists(outdir):
        os.mkdir(outdir)
     
    # Write forecast_df (includes realised)
    forecast.to_csv(outdir / 'forecast.csv', compression='gzip')
    
    # Write model
    model.save_model(outdir / "model.json")
    
    # Write meta data - prediction job and backtest parameters
    # relevant prediction_job attributes
    rel_attrs = ['id','name','model','quantiles']
    rel_pj_dict={key: prediction_job[key] for key in rel_attrs}
    with open(outdir / "configs.yaml", "w") as file:
        documents = yaml.dump({**rel_pj_dict, **backtest_specs}, file)
