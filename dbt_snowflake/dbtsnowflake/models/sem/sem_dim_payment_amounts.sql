select 
    payment_method,
	booking_date,
    count(nights_booked) AS num_booking,
    sum(amount) :: NUMERIC(10,2) AS amount,
    sum(nights_booked) AS nights_booked
from 
    {{ ref('seed_payments') }}
group by 
    1, 2
