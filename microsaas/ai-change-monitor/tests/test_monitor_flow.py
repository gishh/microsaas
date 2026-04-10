from app.models import Change, Monitor, Snapshot
from app.services.monitor_service import run_monitor_check


def test_create_monitor_and_check_flow(client, db_session, monkeypatch):
    responses = [
        "<html><body><h1>Title</h1><p>First version</p></body></html>",
        "<html><body><h1>Title</h1><p>Second version</p></body></html>",
    ]

    def fake_fetch_page(url: str) -> str:
        return responses.pop(0)

    monkeypatch.setattr("app.services.monitor_service.fetch_page", fake_fetch_page)

    create_response = client.post(
        "/monitors",
        data={"name": "Example", "url": "https://example.com"},
        follow_redirects=False,
    )

    assert create_response.status_code == 303

    monitor = db_session.query(Monitor).one()
    first_result = run_monitor_check(db_session, monitor.id)
    second_result = run_monitor_check(db_session, monitor.id)

    assert first_result["changed"] is False
    assert second_result["changed"] is True
    assert db_session.query(Snapshot).count() == 2
    assert db_session.query(Change).count() == 1


def test_pages_render_and_change_summary_is_visible(client, db_session, monkeypatch):
    responses = [
        "<html><body><h1>Title</h1><p>First version</p></body></html>",
        "<html><body><h1>Title</h1><p>Second version</p></body></html>",
    ]

    def fake_fetch_page(url: str) -> str:
        return responses.pop(0)

    monkeypatch.setattr("app.services.monitor_service.fetch_page", fake_fetch_page)

    dashboard_response = client.get("/")
    assert dashboard_response.status_code == 200
    assert "No monitors yet" in dashboard_response.text

    create_page_response = client.get("/monitors/new")
    assert create_page_response.status_code == 200
    assert "Create Monitor" in create_page_response.text

    create_response = client.post(
        "/monitors",
        data={"name": "Example", "url": "https://example.com"},
        follow_redirects=False,
    )
    assert create_response.status_code == 303

    monitor = db_session.query(Monitor).one()

    detail_response = client.get(f"/monitors/{monitor.id}")
    assert detail_response.status_code == 200
    assert "Check now" in detail_response.text

    first_check_response = client.post(f"/monitors/{monitor.id}/check", follow_redirects=True)
    assert first_check_response.status_code == 200
    assert db_session.query(Snapshot).count() == 1

    second_check_response = client.post(f"/monitors/{monitor.id}/check", follow_redirects=True)
    assert second_check_response.status_code == 200
    assert "Detected 1 added line(s) and 1 removed line(s)." in second_check_response.text

    change = db_session.query(Change).one()
    change_response = client.get(f"/changes/{change.id}")
    assert change_response.status_code == 200
    assert "Readable diff" in change_response.text
    assert "Detected 1 added line(s) and 1 removed line(s)." in change_response.text
