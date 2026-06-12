# Domain Glossary

## NotificationEvent

A record of one notification delivery attempt to one user. One business event (e.g. an order
status change) produces one `NotificationEvent` row per recipient.

**Fields:**
- `event_type` — what happened (see *NotificationEventType*)
- `recipient` — FK to the single user this row targets
- `payload` — JSON blob carrying the data the frontend needs to render the notification
  (e.g. `order_uuid`, `new_status`, `order_total`)
- `created_at` — when the row was created
- `sent_at` — when `group_send` was called; NULL means not yet attempted
- `read_at` — when the user acknowledged the notification via the REST endpoint; NULL means unread
- `status` — delivery state: `created`, `sent`, or `failed` (see *NotificationStatus*)

`sent` means `group_send` was called without raising an exception. It does **not** mean the user's
browser received the message — that is unknowable at this layer. `read_at` is the authoritative
signal that the user saw the notification.

## NotificationEventType

A separate enum from `Order.OrderStatus`. Values:

- `purchase.order.created`
- `purchase.order.buyer.rejected`
- `purchase.order.supplier.rejected`
- `purchase.order.approved`
- `purchase.order.shipped`
- `purchase.order.received`

`purchase.order.created` is distinct from the `DRAFT` order status — it represents the business
event of an order being placed, not the technical state of the order row.
`buyer.rejected` and `supplier.rejected` are kept distinct because they mean opposite things to
each recipient and trigger in different service methods.

## NotificationStatus

The delivery state of a single `NotificationEvent` row.

- `created` — row exists, WS push not yet attempted
- `sent` — `group_send` was called without exception
- `failed` — the `on_commit` callback threw before `group_send` could be called

## Order

A purchase agreement between a Buyer and a Supplier, created from the Buyer's cart. One Order
is created per distinct Supplier in the cart at checkout time.

## OrderStatus

The lifecycle state of an Order. Distinct from *NotificationEventType*.

- `purchase.order.draft` — just created, not yet acted on
- `purchase.order.buyer.rejected` — Buyer cancelled
- `purchase.order.supplier.rejected` — Supplier declined
- `purchase.order.approved` — Supplier accepted
- `purchase.order.shipped` — Supplier has shipped
- `purchase.order.received` — Buyer confirmed receipt

## Buyer

The User who places an Order. Identified via `Order.buyer` FK.

## Supplier

The User who owns the Products in an Order. Identified via `Order.supplier` FK.
