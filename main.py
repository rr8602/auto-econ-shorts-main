from common.time_utils import get_kst_hour
from longform.us_longform import run_us_longform
from longform.kr_longform import run_kr_longform
from shorts.shorts_pipeline import run_shorts_pipeline

def run_pipeline():
    hour = get_kst_hour()
    print(f"⏰ KST {hour}시")

    # if hour == 8:
    #     run_us_longform()
    # elif hour == 15:
    #     run_kr_longform()
    # elif hour in (1, 9, 17):
    #     run_shorts_pipeline()
    # else:
    #     print("⏸ 실행 없음")
    run_us_longform()


if __name__ == "__main__":
    run_pipeline()
