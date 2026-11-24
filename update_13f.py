import json
import traceback
from datetime import datetime, timezone
from edgar import Company, set_identity

set_identity("Alpha13F_Tracker admin@alpha13f-tracker.io")

INVESTORS_META = [
    {"id": "buffett", "cik": "0001067983", "name": "워런 버핏", "enName": "Warren Buffett", "firm": "Berkshire Hathaway", "style": "value", "styleLabel": "가치투자", "philosophy": "경제적 해자를 가진 우량 기업의 장기 보유 및 현금흐름 중시"},
    {"id": "dalio", "cik": "0001350694", "name": "레이 달리오", "enName": "Ray Dalio", "firm": "Bridgewater Associates", "style": "macro", "styleLabel": "매크로/헤지", "philosophy": "올웨더(All Weather) 리스크 패리티 및 글로벌 거시경제 분산"},
    {"id": "ackman", "cik": "0001336528", "name": "빌 애크먼", "enName": "Bill Ackman", "firm": "Pershing Square Capital", "style": "activist", "styleLabel": "행동주의", "philosophy": "소수 우량 기업에 대한 초집중 투자 및 지배구조 개선"},
    {"id": "burry", "cik": "0001649339", "name": "마이클 버리", "enName": "Michael Burry", "firm": "Scion Asset Management", "style": "value", "styleLabel": "가치투자", "philosophy": "극단적 저평가 역발상 가치투자 및 거시적 리스크 헷징"},
    {"id": "druckenmiller", "cik": "0001536411", "name": "스탠리 드러켄밀러", "enName": "Stanley Druckenmiller", "firm": "Duquesne Family Office", "style": "macro", "styleLabel": "매크로/헤지", "philosophy": "유동성 사이클과 AI·기술 패러다임 변화에 따른 유연한 베팅"},
    {"id": "wood", "cik": "0001697748", "name": "캐시 우드", "enName": "Cathie Wood", "firm": "ARK Investment Management", "style": "growth", "styleLabel": "성장/혁신", "philosophy": "AI, 유전체학, 로보틱스, 블록체인 등 파괴적 혁신 기업 집중"},
    {"id": "griffin", "cik": "0001423053", "name": "켄 그리핀", "enName": "Ken Griffin", "firm": "Citadel Advisors", "style": "quant", "styleLabel": "퀀트", "philosophy": "멀티 전략 퀀트 트레이딩, 시장 조성 및 초단기 알파 추구"},
    {"id": "simons", "cik": "0001037389", "name": "짐 사이먼스", "enName": "Jim Simons", "firm": "Renaissance Technologies", "style": "quant", "styleLabel": "퀀트", "philosophy": "수학적 통계 모델과 알고리즘을 활용한 비선형 시장 패턴 포착"},
    {"id": "tepper", "cik": "0001656456", "name": "데이비드 테퍼", "enName": "David Tepper", "firm": "Appaloosa Management", "style": "macro", "styleLabel": "매크로/헤지", "philosophy": "부실 자산 및 거시적 정책 전환기 고수익 기회 포착"},
    {"id": "coleman", "cik": "0001167483", "name": "체이스 콜먼", "enName": "Chase Coleman", "firm": "Tiger Global Management", "style": "growth", "styleLabel": "성장/혁신", "philosophy": "글로벌 인터넷·소프트웨어·AI 생태계 승자 독식 기업 장기 투자"},
    {"id": "loeb", "cik": "0001040273", "name": "댄 롭", "enName": "Daniel Loeb", "firm": "Third Point", "style": "activist", "styleLabel": "행동주의", "philosophy": "이벤트 드리븐 및 행동주의적 개입을 통한 기업 가치 제고"},
    {"id": "icahn", "cik": "0000921669", "name": "칼 아이칸", "enName": "Carl Icahn", "firm": "Icahn Capital Management", "style": "activist", "styleLabel": "행동주의", "philosophy": "저평가된 자산주 경영권 압박 및 자사주 매입·배당 확대 요구"},
    {"id": "klarman", "cik": "0001061768", "name": "세스 클라만", "enName": "Seth Klarman", "firm": "Baupost Group", "style": "value", "styleLabel": "가치투자", "philosophy": "안전마진(Margin of Safety) 극대화 및 하방 리스크 철저 방어"},
    {"id": "marks", "cik": "0000949509", "name": "하워드 막스", "enName": "Howard Marks", "firm": "Oaktree Capital Management", "style": "value", "styleLabel": "가치투자", "philosophy": "시장 사이클 이해와 부실채권·고수익 크레딧 중심의 방어적 투자"},
    {"id": "li_lu", "cik": "0001709323", "name": "리 루", "enName": "Li Lu", "firm": "Himalaya Capital Management", "style": "value", "styleLabel": "가치투자", "philosophy": "찰리 멍거의 파트너, 소수 초우량 가치주 장기 집중 보유"},
    {"id": "pabrai", "cik": "0001549575", "name": "모니시 파브라이", "enName": "Mohnish Pabrai", "firm": "Dalal Street", "style": "value", "styleLabel": "가치투자", "philosophy": "단순하고 예측 가능한 비즈니스의 복제(Cloning) 및 집중 투자"},
    {"id": "greenblatt", "cik": "0001510387", "name": "조엘 그린블라트", "enName": "Joel Greenblatt", "firm": "Gotham Asset Management", "style": "quant", "styleLabel": "퀀트", "philosophy": "마법공식(높은 자본수익률 + 높은 이익수익률) 기반 롱숏 전략"},
    {"id": "singer", "cik": "0001048445", "name": "폴 싱어", "enName": "Paul Singer", "firm": "Elliott Investment Management", "style": "activist", "styleLabel": "행동주의", "philosophy": "글로벌 행동주의 캠페인, 구조조정 및 테크 기업 가치 극대화"},
    {"id": "einhorn", "cik": "0001079114", "name": "데이비드 아인혼", "enName": "David Einhorn", "firm": "Greenlight Capital", "style": "value", "styleLabel": "가치투자", "philosophy": "거시경제 인플레이션 수혜주 및 현금흐름 대비 저평가 종목 매수"},
    {"id": "laffont", "cik": "0001135730", "name": "필립 라폰트", "enName": "Philippe Laffont", "firm": "Coatue Management", "style": "growth", "styleLabel": "성장/혁신", "philosophy": "데이터 사이언스 기반의 글로벌 테크·AI·클라우드 성장주 투자"}
]

def to_quarter_label(date_str):
    try:
        dt = datetime.strptime(str(date_str)[:10], "%Y-%m-%d")
        q = (dt.month - 1) // 3 + 1
        return f"{dt.year} Q{q}"
    except Exception:
        return str(date_str)[:10]

def extract_table(obj):
    if obj is None:
        return None
    for attr in ("infotable", "holdings"):
        val = getattr(obj, attr, None)
        if val is not None and not getattr(val, "empty", True):
            return val
    if callable(getattr(obj, "holdings_view", None)):
        try:
            hv = obj.holdings_view()
            if hv is not None and not getattr(hv, "empty", True):
                return hv
        except Exception:
            pass
    return None

def parse_infotable(filing):
    df = extract_table(filing.obj())
    if df is None or df.empty:
        return None

    df = df.copy()
    col_map = {str(c).lower(): c for c in df.columns}
    cusip_col = col_map.get("cusip")
    issuer_col = col_map.get("issuer") or col_map.get("nameofissuer") or col_map.get("company")
    ticker_col = col_map.get("ticker")
    val_col = col_map.get("value") or col_map.get("market_value") or col_map.get("marketvalue")
    shares_col = col_map.get("shares") or col_map.get("sshprnamt")

    if not val_col:
        return None

    df["ValueNum"] = df[val_col].fillna(0).astype(float)
    df["SharesNum"] = df[shares_col].fillna(0).astype(float) if shares_col else 0.0

    multiplier = 1000 if df["ValueNum"].sum() < 50_000_000 else 1
    df["ValueUSD"] = df["ValueNum"] * multiplier

    df["CleanTicker"] = df[ticker_col].fillna("").astype(str).str.strip() if ticker_col else ""
    df["CleanIssuer"] = df[issuer_col].fillna("Unknown").astype(str).str.strip() if issuer_col else "Unknown"
    df["CleanCusip"] = df[cusip_col].fillna("").astype(str).str.strip() if cusip_col else ""
    df["Key"] = df["CleanCusip"].where(df["CleanCusip"] != "", df["CleanIssuer"])

    grouped = df.groupby("Key", as_index=False).agg({
        "CleanTicker": "first",
        "CleanIssuer": "first",
        "ValueUSD": "sum",
        "SharesNum": "sum"
    })
    return grouped

def fetch_all_13f():
    results = []
    MAX_QUARTERS = 8

    for meta in INVESTORS_META:
        try:
            print(f"[{meta['enName']}] 조회 시작...")
            company = Company(meta["cik"])
            filings = company.get_filings(form="13F-HR")
            if not filings or len(filings) == 0:
                print(f"  -> 13F-HR 공시 없음: {meta['enName']}")
                continue

            period_filings = {}
            for f in filings[:MAX_QUARTERS * 2]:
                p = str(getattr(f, "period_of_report", getattr(f, "filing_date", "")))[:10]
                if p and p not in period_filings:
                    period_filings[p] = f
                if len(period_filings) >= MAX_QUARTERS:
                    break

            sorted_periods = sorted(period_filings.keys())
            quarterly_snapshots = []

            for p in sorted_periods:
                f = period_filings[p]
                parsed = parse_infotable(f)
                if parsed is not None and not parsed.empty:
                    total_val = parsed["ValueUSD"].sum()
                    parsed["Weight"] = (parsed["ValueUSD"] / total_val * 100).round(2) if total_val > 0 else 0
                    quarterly_snapshots.append({
                        "period": p,
                        "quarter": to_quarter_label(p),
                        "filingDate": str(getattr(f, "filing_date", p))[:10],
                        "data": parsed.set_index("Key").to_dict("index")
                    })

            if not quarterly_snapshots:
                print(f"  -> 파싱 가능한 테이블 없음: {meta['enName']}")
                continue

            all_keys = set()
            for snap in quarterly_snapshots:
                all_keys.update(snap["data"].keys())

            history_by_key = {}
            for key in all_keys:
                first_bought = None
                add_events = []
                trim_events = []
                timeline = []
                prev_shares = 0

                for idx, snap in enumerate(quarterly_snapshots):
                    item = snap["data"].get(key)
                    q_label = snap["quarter"]
                    f_date = snap["filingDate"]

                    if item and (item["SharesNum"] > 0 or item["ValueUSD"] > 0):
                        curr_shares = item["SharesNum"]
                        curr_weight = item["Weight"]

                        if prev_shares == 0:
                            if first_bought is None:
                                first_bought = f"{q_label} ({f_date} 공시)"
                            action = "신규 매수" if idx > 0 else "보유 확인"
                            timeline.append({
                                "quarter": q_label,
                                "filingDate": f_date,
                                "action": action,
                                "shares": int(curr_shares),
                                "weight": curr_weight,
                                "changePct": None
                            })
                        else:
                            diff_pct = round(((curr_shares - prev_shares) / prev_shares) * 100, 1) if prev_shares > 0 else 0.0
                            if diff_pct >= 1.0:
                                action = "추가 매수"
                                add_events.append(f"{q_label} (+{diff_pct}%)")
                            elif diff_pct <= -1.0:
                                action = "비중 축소"
                                trim_events.append(f"{q_label} ({diff_pct}%)")
                            else:
                                action = "비중 유지"

                            timeline.append({
                                "quarter": q_label,
                                "filingDate": f_date,
                                "action": action,
                                "shares": int(curr_shares),
                                "weight": curr_weight,
                                "changePct": diff_pct
                            })
                        prev_shares = curr_shares
                    else:
                        if prev_shares > 0:
                            trim_events.append(f"{q_label} (전량 매도)")
                            timeline.append({
                                "quarter": q_label,
                                "filingDate": f_date,
                                "action": "전량 매도",
                                "shares": 0,
                                "weight": 0,
                                "changePct": -100.0
                            })
                        prev_shares = 0

                if quarterly_snapshots[0]["data"].get(key):
                    first_bought = f"{quarterly_snapshots[0]['quarter']} 이전부터 보유"

                history_by_key[key] = {
                    "firstBought": first_bought,
                    "addHistory": add_events[-4:],
                    "trimHistory": trim_events[-4:],
                    "timeline": list(reversed(timeline))
                }

            latest_snap = quarterly_snapshots[-1]
            latest_df = parse_infotable(period_filings[latest_snap["period"]]).sort_values(by="ValueUSD", ascending=False)
            total_aum_usd = latest_df["ValueUSD"].sum()

            top_holdings = []
            for _, row in latest_df.head(20).iterrows():
                key = row["Key"]
                ticker = row["CleanTicker"] if row["CleanTicker"] else row["CleanIssuer"][:6].upper()
                val_usd = float(row["ValueUSD"])
                weight = round((val_usd / total_aum_usd) * 100, 2) if total_aum_usd > 0 else 0
                hist = history_by_key.get(key, {})

                top_holdings.append({
                    "ticker": ticker,
                    "name": row["CleanIssuer"].title(),
                    "weight": weight,
                    "valueB": round(val_usd / 1e9, 3),
                    "shares": int(row["SharesNum"]),
                    "firstBought": hist.get("firstBought", "-"),
                    "addHistory": hist.get("addHistory", []),
                    "trimHistory": hist.get("trimHistory", []),
                    "timeline": hist.get("timeline", [])
                })

            top5_weight = round(sum(h["weight"] for h in top_holdings[:5]), 1)

            results.append({
                "id": meta["id"],
                "cik": meta["cik"],
                "name": meta["name"],
                "enName": meta["enName"],
                "firm": meta["firm"],
                "style": meta["style"],
                "styleLabel": meta["styleLabel"],
                "philosophy": meta["philosophy"],
                "filingDate": latest_snap["filingDate"],
                "reportPeriod": latest_snap["period"],
                "trackedQuarters": len(quarterly_snapshots),
                "aumB": round(total_aum_usd / 1e9, 2),
                "holdingsCount": len(latest_df),
                "top5Weight": top5_weight,
                "holdings": top_holdings
            })
            print(f"  -> 성공: {meta['enName']} ({len(latest_df)}종목)")
        except Exception as e:
            print(f"Error fetching {meta['enName']}: {e}")
            traceback.print_exc()

    output = {
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "investors": results
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"총 {len(results)}명 저장 완료!")

if __name__ == "__main__":
    fetch_all_13f()
