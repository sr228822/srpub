# Lets use windowed bucketeds, say 1 minute each
# for each bucket, we'll track users who have had activity in that bucket
# for each user, we'll track the first and last activity within the bucket
# We could expire/page-out older buckets to free up memory as an optimization


def update(rng, timestamp):
    # events can arrive slightly out of order, so can't guarentee this timestamp is greater
    # than previous ones
    return (min(rng[0], timestamp), max(rng[1], timestamp))


class UserActivityTracker:
    def __init__(self, sessionTimeoutMinutes: int = 5):
        self.session_timeout = sessionTimeoutMinutes

        self.buckets = {}

        # theres an assumption here that BUCKETSIZE is small enough relative to sessionTimeoutMinutes
        # that if a user has an event in 2 adjascent buckets they will have an active session spanning them
        self.BUCKETSIZE = 60
        assert (2 * self.BUCKETSIZE) < (sessionTimeoutMinutes * 60)

    def recordEvent(self, timestamp, userId, eventType):
        # events might arrive slightly out of order for different users, but generally increasing

        timeBucket = int(timestamp / self.BUCKETSIZE)
        if timeBucket not in self.buckets:
            self.buckets[timeBucket] = {}

        # First occurance of user in this bucket
        if userId not in self.buckets[timeBucket]:
            self.buckets[timeBucket][userId] = (timestamp, timestamp)
        else:
            self.buckets[timeBucket][userId] = update(
                self.buckets[timeBucket][userId], timestamp
            )

        # Update the previous and next buckets as well
        if userId in self.buckets.get(timeBucket - 1, {}):
            self.buckets[timeBucket - 1][userId] = update(
                self.buckets[timeBucket - 1][userId], timestamp
            )
        if userId in self.buckets.get(timeBucket + 1, {}):
            self.buckets[timeBucket + 1][userId] = update(
                self.buckets[timeBucket + 1][userId], timestamp
            )

        # debug print
        print(f"\n\nrecorded {timestamp} {userId} {eventType}")
        for bucket_id in self.buckets.keys():
            bucket = self.buckets[bucket_id]
            for user_id in bucket.keys():
                print(f"{bucket_id} {user_id} {bucket[user_id]}")

    def getActiveUsers(self, queryTimestamp):
        # Returns the set of userids who were active at queryTimestamp
        # aka had one event in the window [querytimetsmap - sessiontimeoutseconds, queryTimestamp]

        window_start = queryTimestamp - (self.session_timeout * 60)
        bucket_start = int(window_start / self.BUCKETSIZE)

        window_end = queryTimestamp
        bucket_end = int(queryTimestamp / self.BUCKETSIZE)

        users = set()
        for bucket_id in range(bucket_start, bucket_end + 1):
            for user_id, active_range in self.buckets.get(bucket_id, {}).items():
                # user was active for range active_range
                if (
                    active_range[1] > window_start and active_range[1] <= window_end
                ) or (active_range[0] > window_start and active_range[0] <= window_end):
                    users.add(user_id)

        return users


tracker = UserActivityTracker(sessionTimeoutMinutes=5)
tracker.recordEvent(100, "userA", "click")
tracker.recordEvent(150, "userB", "view")
tracker.recordEvent(350, "userA", "type")  # userA's session continues
tracker.recordEvent(400, "userB", "click")  # userB's session continues
tracker.recordEvent(800, "userA", "view")  # New session for userA starts
tracker.recordEvent(900, "userC", "login")

print("200 should be A,B")
print(tracker.getActiveUsers(200))

print("450 should be A,B")
print(tracker.getActiveUsers(450))

print("700 should be none")
print(tracker.getActiveUsers(700))


print("850 should be A")
print(tracker.getActiveUsers(850))

print("1000 should be A,C")
print(tracker.getActiveUsers(1000))
