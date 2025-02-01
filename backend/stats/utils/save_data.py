"""
@author: Joseph A.
Description: Utility functions for saving statistical data to JSON files
"""
import os
import json

def save_json_data(data, filename: str, base_path: str, data_type: str = 'distribution'):
    """Save pandas data (Series or DataFrame) to a JSON file.

    Args:
        data (Union[pd.Series, pd.DataFrame]): Data to save:
            - Series for distribution data
            - DataFrame for ratings data (must have 'mean' and 'count' columns)
        filename (str): Name of the output file (without extension)
        base_path (str): Directory path where to save the JSON file
        data_type (str, optional):Type of data to save ('distribution' or 'ratings'). 
            Defaults to 'distribution'.

    Raises:
        ValueError: If data_type is 'ratings' but DataFrame doesn't have required columns
    """
    os.makedirs(base_path, exist_ok=True)

    if data_type == 'distribution':
        json_data = {
            'data': data.to_dict(),
            'total': int(data.sum()),
            'count': len(data)
        }
    else:  # ratings
        if not all(col in data.columns for col in ['mean', 'count']):
            raise ValueError("Ratings DataFrame must have 'mean' and 'count' columns")

        json_data = {
            'data': data.round(2).to_dict(orient='index'),
            'total_ratings': int(data['count'].sum()),
            'average_rating': float(data['mean'].mean().round(2))
        }

    with open(os.path.join(base_path, f'{filename}.json'), 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
