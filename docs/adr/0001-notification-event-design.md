# ADR 0001: NotificationEvent design for order status push notifications

## Status
Accepted

## Context

Orders have two participants (Buyer and Supplier) who both need to be informed when order status
changes. The backend already has a `notifications` app with a `BroadcastNotification` model
(scheduled blasts to everyone) and a `NotificationConsumer` WebSocket consumer (room-based,
unauthenticated, leftover from a chat requirement). Neither fit the per-user targeted delivery
needed here.

The frontend needs both real-time push (WebSocket) and a catch-up path (REST) for users who were
offline when an event fired.

## Decisions

| Question | Decision | Reason |
|---|---|---|
| Rows per event | One `NotificationEvent` row per recipient | Per-recipient delivery state cannot be tracked in a single row with multiple recipients |
| Read state | Separate `read_at` timestamp field | Delivery state (`status`) and read state are independent facts; overloading `status` with a `read` value collapses two axes into one |
| Payload | JSONField on `NotificationEvent` | Small, stable data (order UUID, new status, total); generic FK adds a join with no normalization benefit |
| `event_type` enum | Separate from `Order.OrderStatus` | `purchase.order.created` is a business event with no matching `OrderStatus` value; the enum conveys what happened, not the current state |
| Rejection event types | `buyer.rejected` and `supplier.rejected` kept distinct | They mean opposite things to each recipient and are triggered by different service methods |
| `status: sent` meaning | `group_send` called without exception | Provable receipt requires a consumer DB write on every message; the REST fallback already covers the offline case |
| Trigger mechanism | `transaction.on_commit` → inline `async_to_sync(channel_layer.group_send)` | `on_commit` decouples notification failure from order status change failure; inline push avoids a separate worker for this use case |
| Channel layer backend | `channels_redis` (Redis) | The officially supported, actively maintained Channels backend. `channels_rabbitmq` is unmaintained. Postgres LISTEN/NOTIFY would avoid Redis but holds one async DB connection per open WS connection — unacceptable at scale. In-memory layer breaks under multi-worker Daphne. Redis is the correct call. |
| WS auth | JWT verified in `connect()` | Reuses existing JWT infrastructure; one-time ticket endpoint adds round-trip and surface area |
| WS URL | Per-user UUID, regex updated to allow hyphens | Room-based pattern was a chat leftover; per-user connection matches the targeted delivery model |
| Offline delivery | REST endpoint returns rows where `read_at IS NULL` | WS push is best-effort; REST is the authoritative catch-up path |
| Payload shape | `{ "order_uuid": "...", "order_total": 42.0 }` | `event_type` is already a top-level column; payload carries only order-specific context not otherwise on the row |
| Notification message | Derived by frontend from `event_type` using i18n files | Backend has no locale context; i18n belongs at the presentation layer where `messages/en.json` and `messages/gr.json` already live |
| Mark as read | `PATCH /api/notifications/read/` with `{ "ids": [...] }` — batched, debounced | Intersection Observer collects visible IDs; debounce collapses scroll events into one request per pause |
| Pagination | DRF `CursorPagination` on `created_at DESC` | Stable under new arrivals — page-number pagination shifts items when new notifications are inserted during scroll |

## Consequences

- `BroadcastNotification` model and its Celery task are separate concerns and remain unchanged.
- The existing `NotificationConsumer` is replaced entirely — room-based pattern removed, per-user
  UUID connection with JWT auth on `connect()`. URL regex changed to `[0-9a-f-]{36}` to support UUIDs.
- `CHANNEL_LAYERS` in `settings.py` must be configured with `channels_redis`.
- `channels_redis` added to dependencies. Redis must be available (default `localhost:6379`).
- `order_created_handler` and `order_status_changed_handler` signal stubs in `orders/models.py`
  are removed; notification creation moves to `OrderService` via `transaction.on_commit`.
- `OrderService.change_order_status` and `place_draft_orders` each register an `on_commit`
  callback that creates `NotificationEvent` rows and calls `group_send` for each recipient.
- Three REST endpoints: `GET /api/notifications/` (cursor-paginated, unread-first),
  `GET /api/notifications/unread-count/` (lightweight count for the bell badge),
  `PATCH /api/notifications/read/` (bulk mark-as-read by ID list).
- Frontend uses `useInfiniteQuery` with cursor pagination and Intersection Observer to mark
  notifications read as they scroll into view, batched and debounced.
