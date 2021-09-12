import math
import datetime

def get_diff_days(str_date1, str_date2):
  d1 = datetime.datetime.strptime(str_date1, "%Y-%m-%d").date()
  d2 = datetime.datetime.strptime(str_date2, "%Y-%m-%d").date()
  return abs(d2 - d1).days

def get_score(total, average):
  """
  Score starting from 0 and scale using logorithm based 10
  1 invoice get 1 point. But after x days until next invoice, 
  point will be decreased by 1
  """
  POINT_SCALE = 30 # days (could be changed to any preferred length)
  average_point = average/POINT_SCALE
  return round(math.log10(total - average_point), 4) if total > average_point else 0