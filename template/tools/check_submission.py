"""Poll Kaggle submission status until scoring completes."""

import time
from datetime import datetime, timezone

import click


@click.command()
@click.option("--competition", default="{{ kaggle_competition }}", help="Kaggle competition slug.")
@click.option("--interval", default=60, help="Polling interval in seconds.")
def main(competition: str, interval: int) -> None:
    """Check the latest Kaggle submission status."""
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()

    submissions = api.competition_submissions(competition)
    if not submissions:
        click.echo("No submissions found.", err=True)
        raise SystemExit(1)

    latest = submissions[0]
    latest_ref = latest.ref
    submit_time = latest.date
    if submit_time.tzinfo is None:
        submit_time = submit_time.replace(tzinfo=timezone.utc)
    click.echo(f"Tracking submission: {latest_ref}")

    status = ""
    public_score = ""
    while status != "complete":
        found = False
        for sub in api.competition_submissions(competition):
            if sub.ref == latest_ref:
                status = sub.status
                public_score = sub.publicScore
                found = True
                break

        if not found:
            click.echo("Submission no longer found. It may have been deleted.", err=True)
            raise SystemExit(1)

        now = datetime.now(timezone.utc)
        elapsed_min = int((now - submit_time).total_seconds() / 60) + 1

        if status == "complete":
            click.echo(f"\rCompleted in ~{elapsed_min} min, Public LB: {public_score}")
        else:
            click.echo(f"\rElapsed: {elapsed_min} min ...", nl=False)
            time.sleep(interval)


if __name__ == "__main__":
    main()
