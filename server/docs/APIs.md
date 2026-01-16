# FitTrack API Documentation

Base URL: `/api`

## Endpoints

### Health
- `GET /api/health` - Health check

### Members
- `GET /api/members` - List all members
- `POST /api/members` - Create member
- `GET /api/members/<id>` - Get member
- `PUT /api/members/<id>` - Update member

### Plans
- `GET /api/plans` - List plans
- `POST /api/plans` - Create plan
- `GET /api/plans/<id>` - Get plan

### Subscriptions
- `GET /api/members/<id>/subscriptions` - Member subscriptions
- `POST /api/members/<id>/subscriptions` - Create subscription
- `GET /api/members/<id>/subscription-status` - Subscription status
- `PATCH /api/subscriptions/<id>/freeze` - Freeze subscription
- `PATCH /api/subscriptions/<id>/unfreeze` - Unfreeze subscription

### Payments
- `GET /api/payments` - List payments
- `POST /api/payments` - Create payment
- `PUT /api/payments/<id>/status` - Update payment status

### Classes
- `GET /api/classes` - List classes
- `POST /api/classes` - Create class
- `GET /api/classes/<id>` - Get class
- `POST /api/classes/<id>/sessions` - Register member
- `DELETE /api/classes/<id>/sessions/<member_id>` - Cancel registration
- `GET /api/classes/<id>/participants` - Class participants
- `GET /api/classes/<id>/stats` - Class statistics

### Check-ins
- `POST /api/checkins` - Record check-in (requires: member role)
- `GET /api/checkins` - List check-ins (requires: reception role)

### Workout Plans
- `POST /api/workout-plans` - Create workout plan
- `GET /api/members/<id>/workout-plans` - Member plans
- `GET /api/members/<id>/workout-plans/active` - Active plan
- `PATCH /api/workout-plans/<id>/active` - Set plan active
- `GET /api/workout-plans/<id>/items` - Plan items
- `GET /api/workout-items/<id>` - Get item
- `PATCH /api/workout-items/<id>` - Update item
- `DELETE /api/workout-items/<id>` - Delete item

## Architecture

```
Routes (HTTP) → Services (Logic) → Models (Database)
```

**Layers:**
- **Routes**: Request/response handling
- **Services**: Business rules & validation
- **Models**: Database schema & ORM
