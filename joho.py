def calculate_fuel_efficiency(distance_km, fuel_liter):
    """燃費(km/L)を計算する関数"""
    return distance_km / fuel_liter


def main():
    print("===== 車の燃費計算アプリ =====")

    # 入力
    try:
        distance = float(input("走行距離（km）："))
        fuel = float(input("給油量（L）："))
    except ValueError:
        print("数字を入力してください。")
        return

    # 0除算の防止
    if fuel <= 0:
        print("給油量は0より大きい値を入力してください。")
        return

    # 計算
    efficiency = calculate_fuel_efficiency(distance, fuel)

    # 結果
    print(f"\n燃費は **{efficiency:.2f} km/L** です！")
    print("===============================")


if __name__ == "__main__":
    main()
