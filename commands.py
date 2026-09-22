import random
from objects import Star

def execute_command(input_text):
    command = input_text.strip().lower()
    r_dir = random.choice([1, -1])
    
    if command == "milkyway":
        new_stars = [Star("spiral", arms=2, max_dist=1600, spin=0.003, direction=r_dir) for _ in range(150)]
        return new_stars, "MilkyWay", True
    elif command == "andromeda":
        new_stars = [Star("spiral", arms=3, max_dist=2000, spin=0.002, direction=r_dir) for _ in range(250)]
        return new_stars, "Andromeda", True
    elif command == "sombrero":
        new_stars = [Star("sombrero", direction=r_dir) for _ in range(180)]
        return new_stars, "Sombrero", True
    elif command == "cluster":
        new_stars = [Star("cluster", direction=r_dir) for _ in range(80)]
        return new_stars, "Star Cluster", True
    elif command == "random":
        r_arms = random.randint(2, 6)
        r_stars = random.randint(80, 200)
        r_spin = random.uniform(0.002, 0.006)
        r_size = random.randint(1200, 1800)
        new_stars = [Star("spiral", arms=r_arms, max_dist=r_size, spin=r_spin, direction=r_dir) for _ in range(r_stars)]
        return new_stars, f"Random (Arms: {r_arms})", True
    elif command == "meteor":
        # Возвращаем None для звезд, чтобы главный файл знал: нужно просто доспавнить метеоры
        return None, "meteor", True
    elif command == "exit":
        return None, "exit", True
        
    return None, None, False
