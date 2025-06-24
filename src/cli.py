import argparse

from core.calculate_uuid import calculate_genuine_uuid, calculate_offline_uuid
from core.transfer_palyerdata import backup_file, list_available_players, transfer_playerdata


def main():
    parser = argparse.ArgumentParser(description='Minecraft Utility CLI')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subparser for UUID calculation
    uuid_parser = subparsers.add_parser('uuid', help='Calculate UUID based on username')
    uuid_parser.add_argument('username', type=str, help='The username to calculate the UUID for')
    uuid_parser.add_argument('--offline', action='store_true', help='Calculate offline UUID')

    # Subparser for saves data transfer
    save_parser = subparsers.add_parser('save', help='Saves player data tool')
    save_parser.add_argument('path', type=str, help='Path to the saves directory')
    save_parser.add_argument('-i', '--uuid', type=str, help='UUID of the player to transfer data for')
    save_parser.add_argument('--backup', action='store_true', help='Backup level.dat before transferring data')
    save_parser.add_argument('-l', '--list', action='store_true', help='List available players in the saves directory')

    args = parser.parse_args()

    # Handle the commands
    if args.command == 'uuid':
        if args.offline:
            uuid = calculate_offline_uuid(args.username)
        else:
            uuid = calculate_genuine_uuid(args.username)
        print(f'Calculated UUID for {args.username}: {uuid}')

    elif args.command == 'save':
        players = list_available_players(args.path)

        if args.list:
            if players:
                print('Available players:')
                for uuid, name in players:
                    if name:
                        print(f'    {uuid} ({name})')
                    else:
                        print(f'    {uuid}')
            else:
                print('No players found.')
        else:
            if not args.uuid:
                print('Error: UUID is required for data transfer.')
                return

            if not any(uuid == args.uuid for uuid, _ in players):
                print(f'Warning: UUID {args.uuid} not found in the saves directory.')
                print('Available players:')
                for uuid, name in players:
                    if name:
                        print(f'    {uuid} ({name})')
                    else:
                        print(f'    {uuid}')

                response = input('Do you want to continue with the transfer? (y/N): ')
                if response.lower() != 'y':
                    print('Transfer cancelled.')
                    return

            if args.backup:
                backup_file(args.path)

            success = transfer_playerdata(args.path, args.uuid)
            if success:
                print('Player data transfer completed successfully.')
            else:
                print('Player data transfer failed.')
    else:
        print('Unknown command. Use -h, --help for usage information.')

    pass
