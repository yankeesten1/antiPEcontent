import argparse

from .config import Settings
from .service import make_batch
from .store import Store
from .web import serve
from .pilot import export_pilot, DEFAULT_BATCH
from .social import export_social
from .voice import DEFAULT_VOICE


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
    social.add_argument('--audio-preview', action='store_true', help='Add local neural narration and original music; requires optional voice setup and FFmpeg')
    social.add_argument('--voice', default=DEFAULT_VOICE, help='Local stock voice key; default is the user-selected af_heart')
    social.add_argument('--voice-speed', type=float, default=1.0, help='Narration speed, 0.8–1.2')
    voice = commands.add_parser('prepare-voice', help='Download and checksum-verify the optional local neural voice model')
    voice.add_argument('--directory')
    comparison = commands.add_parser('compare-voices', help='Export six same-script local voice auditions; no paid API calls')
    comparison.add_argument('--output', default='.local/pilot/voice-comparison')
    args = parser.parse_args()
    if args.command == 'compare-voices':
        from .voice_comparison import export_voice_comparison
        print(f'Created voice auditions: {export_voice_comparison(args.output)}')
        return
    if args.command == 'prepare-voice':
        from .voice import prepare_voice
        print(f'Verified voice model cache: {prepare_voice(args.directory)}')
        return
    if args.command == 'social':
        print(f'Created social media concept: {export_social(args.output, args.video, args.audio_preview, args.voice, args.voice_speed)}')
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
