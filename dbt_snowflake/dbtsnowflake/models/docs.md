{% docs dim_hosts_cleansed__host_id %} 
Primary key for the host. 

{% enddocs %}

{% docs dim_hosts_cleansed__host_name %} 
Airbnb host name. 

{% enddocs %}

{% docs dim_hosts_cleansed__is_superhost %} 
Defines whether the hosts is a superhost. 

{% enddocs %}


{% docs dim_listings_hosts__listing_host_id %} 
Subrogate key. 

{% enddocs %}

{% docs dim_listings_hosts__listing_id %} 
The listings's id. References the host table. 

{% enddocs %}

{% docs dim_listings_hosts__host_id %} 
The hosts's id. References the listing table. 

{% enddocs %}



{% docs dim_listings_cleansed__minimum_nights %} 
Minimum number of nights required to rent this property. 

Keep in mind that old listings might have `minimum_nights` set  
to 0 in the source tables. Our cleansing algorithm updates this to `1`. 

{% enddocs %}
