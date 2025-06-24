"""
@author: chillcicada
@date: 2025-06-23

@description: Transfer player data from one Minecraft LAN server host to another player, based on UUIDs. Some codes are inherited from the original code by ideenster.
"""

import os
import shutil
from copy import deepcopy
from typing import List

from nbtlib import nbt


def backup_file(file_path: str) -> str:
    """创建文件备份"""
    backup_path = f'{file_path}.bak'

    if os.path.exists(backup_path):
        print(f'警告：备份文件已存在: {backup_path}')
        response = input('是否覆盖备份？(y/N): ')
        if response.lower() != 'y':
            print('操作已取消')
            return None

    shutil.copy2(file_path, backup_path)
    print(f'已创建备份: {backup_path}')

    return backup_path


def transfer_playerdata(uuid: str, save_path: str) -> bool:
    """使用nbtlib库转移玩家数据"""
    playerdata_path = os.path.join(save_path, 'playerdata', f'{uuid}.dat')

    if not os.path.exists(playerdata_path):
        print(f'错误：找不到玩家数据文件: {playerdata_path}')
        return False

    level_dat_path = os.path.join(save_path, 'level.dat')

    if not os.path.exists(level_dat_path):
        print(f'错误：找不到level.dat文件: {level_dat_path}')
        return False

    try:
        # 读取玩家数据
        print(f'读取玩家数据: {playerdata_path}')
        player_data = nbt.load(playerdata_path)

        # 读取level.dat
        print(f'读取level.dat: {level_dat_path}')
        level_data = nbt.load(level_dat_path)

        # 备份level.dat
        backup_file(level_dat_path)

        # 将玩家数据复制到level.dat中
        print('正在转移玩家数据...')

        # 获取level.dat中的Player标签，并清空它
        player_level_tag = level_data['Data']['Player']
        player_level_tag.clear()

        # 使用copy.deepcopy来逐项复制新的玩家数据
        for key, tag in player_data.items():
            player_level_tag[key] = deepcopy(tag)

        # 保存修改后的level.dat
        print(f'保存修改后的level.dat: {level_dat_path}')
        level_data.save(level_dat_path)

        print('✓ 玩家数据转移完成！')
        return True

    except Exception as e:
        print(f'错误：处理NBT数据时出现问题: {e}')
        print(f'详细错误信息: {type(e).__name__}: {str(e)}')
        return False


def get_player_name_from_nbt(player_data):
    """从NBT数据中提取玩家名称"""
    try:
        # 尝试不同的可能字段
        if hasattr(player_data, 'get'):
            # nbtlib格式
            if 'bukkit' in player_data and 'lastKnownName' in player_data['bukkit']:
                return player_data['bukkit']['lastKnownName']
            elif 'Paper' in player_data and 'LastKnownName' in player_data['Paper']:
                return player_data['Paper']['LastKnownName']
    except Exception:
        return None


def list_available_players(save_path: str) -> List[tuple]:
    """列出可用的玩家UUID和名称"""
    playerdata_dir = os.path.join(save_path, 'playerdata')
    if not os.path.exists(playerdata_dir):
        print('错误：找不到playerdata文件夹')
        return []

    players = []
    for file in os.listdir(playerdata_dir):
        if file.endswith('.dat') and not file.endswith('.dat_old'):
            uuid = file[:-4]  # 移除.dat后缀
            player_name = None

            # 尝试读取玩家名称
            try:
                player_file = os.path.join(playerdata_dir, file)

                with open(player_file, 'rb') as f:
                    player_data = nbt.load(f)
                player_name = get_player_name_from_nbt(player_data)

            except Exception:
                pass  # 忽略读取错误

            players.append((uuid, player_name))

    return players
