# FAQ

### Q: Why not just set static bonuses?

> Static bonuses waste money or arrive too late. SurgeOpt reacts in real time to real conditions.

---

### Q: Is this compatible with Wolt's or DoorDash's stack?

> Yes. SurgeOpt is designed as a modular microservice. Kafka and HTTP APIs make it drop-in friendly.

---

### Q: Can this run on a single laptop?

> Yes. The simulation version uses Docker Compose and runs fine on a laptop with 8 GB RAM.

---

### Q: Can we plug in real data?

> Absolutely. Replace `order_created`, `courier_loc`, and `weather_snap` topics with live data feeds from your platform.