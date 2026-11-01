# Recorded workflow evidence

All .txt files are outputs of commands actually executed on 1 November 2026.

- docker-build.txt: successful image build.
- docker-tests.txt: all seven tests pass in the mounted Docker environment.
- docker-menu.txt: real application session; supplied input sequence is menu-input.txt (piped input is not echoed).
- docker-restart.txt: a second container restores both added product types and stock 20.
- docker-cleanup.txt: build-cache cleanup and final Docker disk summary.
- local-tests.txt: seven tests pass on the host.
- git-workflow.txt: status, staging summary, implementation commit, history and successful push.
- workflow PNGs: browser captures of the raw command transcripts, clearly labeled; HTML sources included. They are not native Terminal captures. Terminal control was unavailable under computer-use policy.
- uml-preview.png: rendered version of uml.svg.

Final evidence packaging is committed separately after the implementation commit shown in the screenshots.
