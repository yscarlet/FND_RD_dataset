"""
데이터셋별 시간대별 평균 노드 개수를, 그래프별 최종 노드 개수 대비 '%'로 환산해
꺾은선 그래프로 그린다. 결과는 percent/ 폴더에 저장된다.

각 그래프에서 시각 t까지 등장한 노드 수를, 그 그래프의 전체(최종) 노드 수로 나눠
백분율로 만든 뒤 데이터셋 내에서 평균낸다.

사용 예:
    python3 plot_node_growth_percent.py --interval 10 --end 480
    python3 plot_node_growth_percent.py --interval 30 --end 2880 --out result.png
    python3 plot_node_growth_percent.py --interval 60 --end 10080 --datasets gossipcop politifact
"""
import argparse
import glob
import os

import matplotlib.pyplot as plt
import numpy as np

from _growth_common import BASE_DIR, DATASET_COLORS, DATASET_DIV

OUT_DIR = os.path.join(BASE_DIR, "percent")


def compute_avg_growth_percent(dataset, div, bins):
    files = glob.glob(os.path.join(BASE_DIR, dataset, "*.npz"))
    percents = np.zeros((len(files), len(bins)))
    for i, f in enumerate(files):
        cur_time = np.load(f, allow_pickle=True)["cur_time"].astype(np.float64) / div
        total_nodes = cur_time.shape[0]
        counts = (cur_time[None, :] <= bins[:, None]).sum(axis=1)
        percents[i] = counts / total_nodes * 100.0
    return percents.mean(axis=0), len(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--interval", type=float, required=True, help="시간 간격 (분)")
    parser.add_argument("--end", type=float, required=True, help="마지막 시간 (분)")
    parser.add_argument("--start", type=float, default=0.0, help="시작 시간 (분, 기본값 0)")
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=list(DATASET_DIV.keys()),
        choices=list(DATASET_DIV.keys()),
        help="그릴 데이터셋 목록 (기본값: 전체)",
    )
    parser.add_argument("--out", default=None, help="저장할 파일 경로 (기본값: percent/avg_node_percent_{start}_{end}_{interval}.png)")
    args = parser.parse_args()

    bins = np.arange(args.start, args.end + args.interval, args.interval)

    fig, ax = plt.subplots(figsize=(11, 6), dpi=150)
    for ds in args.datasets:
        avg, n_graphs = compute_avg_growth_percent(ds, DATASET_DIV[ds], bins)
        ax.plot(bins, avg, label=f"{ds} (n={n_graphs})", color=DATASET_COLORS[ds], linewidth=2)
        print(f"{ds}: n_graphs={n_graphs}, avg@{bins[0]:g}min={avg[0]:.1f}%, avg@{bins[-1]:g}min={avg[-1]:.1f}%")

    ax.set_xlabel("Time since post (minutes)")
    ax.set_ylabel("Average % of final graph size reached")
    ax.set_title(f"Average cumulative node % per graph over time ({args.start:g}-{args.end:g}min, step {args.interval:g}min)")
    ax.set_xlim(args.start, args.end)
    ax.set_ylim(0, 100)
    ax.grid(True, linewidth=0.5, alpha=0.4)
    ax.legend(loc="lower right", frameon=False)
    fig.tight_layout()

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = args.out or os.path.join(
        OUT_DIR, f"avg_node_percent_{args.start:g}_{args.end:g}_{args.interval:g}.png"
    )
    fig.savefig(out_path)
    print("saved to", out_path)


if __name__ == "__main__":
    main()
