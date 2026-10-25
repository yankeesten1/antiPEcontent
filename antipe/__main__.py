import argparse

from .config import Settings
from .service import make_batch
from .store import Store
from .web import serve
from .pilot import export_pilot, DEFAULT_BATCH
from .social import export_social


def main():
    parser = argparse.ArgumentParser(description='Sourced private equity editorial inbox')
    commands = parser.add_subparsers(dest='command', required=True)
    server = commands.add_parser('serve')
    server.add_argument('--host', default='127.0.0.1')
    server.add_argument('--port', type=int, default=8000)
    server.add_argument('--no-schedule', action='store_true')
    generator = commands.add_parser('generate')
    generator.add_argument('--demo', action='store_true')
    generator.add_argument('--retry', action='store_true', help='Explicitly retry a failed daily batch; may incur API charges')
    pilot = commands.add_parser('pilot', help='Export seven offline drafts, graphics and a metrics tracker; no API calls')
    pilot.add_argument('--output', default='.local/pilot/week-01')
    pilot.add_argument('--batch', default=str(DEFAULT_BATCH))
    pilot.add_argument('--launch-assets', action='store_true', help='Include profile assets, an offline editing page and tonight’s checklist')
    social = commands.add_parser('social', help='Render the redesigned introduction carousel and optional motion reel')
    social.add_argument('--output', default='.local/pilot/introduction-v2')
    social.add_argument('--video', action='store_true', help='Also render a 20-second reel; requires FFmpeg')
    args = parser.parse_args()
    if args.command == 'social':
        print(f'Created social media concept: {export_social(args.output, args.video)}')
        return
    if args.command == 'pilot':
        print(f'Created offline launch kit: {export_pilot(args.output, args.batch, args.launch_assets)}')
        return
    settings = Settings.load()
    store = Store(settings.database)
    if args.command == 'serve':
        serve(settings, store, args.host, args.port, not args.no_schedule)
    else:
        print('Created five drafts.' if make_batch(settings, store, demo=args.demo, retry=args.retry) else 'Today’s batch already exists; see inbox status.')


if __name__ == '__main__':
    main()
