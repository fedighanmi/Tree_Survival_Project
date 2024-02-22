import pytest
import math
import numpy as np
from tree_lab import Visualization as vis
from tree_lab import importing as imp


df = imp.import_data()

def compute_stats_t(numbers):
    numbers = [num for num in numbers if not math.isnan(num)]

    if len(numbers) == 0:
        return None  # Return None for an empty list

    # compute the mean
    total_sum = 0
    for num in numbers:
        total_sum += num
    mean = total_sum / len(numbers)

    # compute the standard deviation
    variance = sum((x - mean) ** 2 for x in numbers) / (len(numbers) - 1)
    stand_dev = math.sqrt(variance)

    # compute the minimum and the maximum
    min_value = max_value = numbers[
        0]  # Assume the first element is both min and max

    for num in numbers[1:]:
        if num < min_value:
            min_value = num
        elif num > max_value:
            max_value = num

    # compute the median
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)

    if n % 2 == 0:
        # If the number of elements is even, take the average
        # of the middle two elements
        mid_left = sorted_numbers[n // 2 - 1]
        mid_right = sorted_numbers[n // 2]
        median = (mid_left + mid_right) / 2
    else:
        # If the number of elements is odd, return the middle element
        median = sorted_numbers[n // 2]

    return np.array([mean, stand_dev, min_value, max_value, median])

@pytest.mark.parametrize("col", ['Light_ISF', 'AMF',
                                 'EMF', 'Phenolics', 'Lignin', 'NSC'])
def testing_compute_stats(col):
    assert compute_stats_t(numbers = df[col].values).all() == pytest.approx(
        vis.compute_stats(dataframe = df,
                      selected_columns = [col]).iloc[0].values.all(),
        abs=1e-4)