#' @name functions_crosstab
#' @title Crosstabulate Data into intervals where r >= 5 
#' @author Tim Fraser
#' @param x (numeric) a vector of times to failure
#' @param binsize (numeric) a single integer describing the size of each interval/bin
#' @param cutoff (numeric) a single number describing the cutoff after which to reaggregate the bins.
# We could try to make our own function to do it all...
crosstab = function(x, binsize = 100, cutoff = Inf){
  # Testing Values
  # Product Times to Failure
  # x = c(1,2,2,3,4,5,7,8,9,10,
  #           11,13,15,16,17,17,18,18,18,20,
  #           20,21,21,24,27,29,30,37,40,40,
  #           40,41,46,47,48,52,54,54, 55,55,
  #           64,65,65,65,67,76,76,79,80,80,
  #           82,86,87,89,94,96,100,101,102,104,
  #           105,109,109,120,123,141,150,156,156,161,
  #           164,167,170,178,181,191,193,206,211,212,
  #           214,236,238,240,265,304,317,328,355,363,
  #           365,369,389,404,427,435,500,522,547,889)
  # binsize = 100
  # cutoff = 450
  
  library(dplyr)
  library(ggplot2)
  
  # Initial crosstabulation
  data = tibble(t = x) %>%
    mutate(interval = cut_interval(t, length = binsize))  %>%
    group_by(interval, .drop = FALSE) %>%
    summarize(r_obs = n())
  
  # Get midpoint for each bin
  data1 = data %>%
    mutate(bin = as.numeric(interval)) %>%
    mutate(lower = (bin - 1) * binsize,
           upper = (bin * binsize),
           midpoint = (lower + upper) / 2) 
  
  # Find all rows past the time interval cutoff
  end = data1 %>%
    filter(midpoint >= cutoff) %>%
    slice(1)
  
  # If there are any rows past the time interval cutoff, 
  # reaggregate
  if(nrow(end) > 0){
    # Revise the interval name and bin id  
    data2 = data1 %>%
      mutate(interval = case_when(
        midpoint >= cutoff ~ end$interval,
        TRUE ~ interval
      ),
      bin = case_when(
        midpoint >= cutoff ~ end$bin, 
        TRUE ~ bin)) 
    
    # Get the unique levels out
    levels = data2$interval %>% unique() %>% sort() %>% as.character()
    
    # Update the interval factor levels
    data3 = data2 %>% 
      mutate(interval = factor(interval, levels = levels))
    
    # Aggregate to the new interval levels
    data4 = data3 %>%
      group_by(bin, interval) %>%
      summarize(r_obs = sum(r_obs))
    
    # Calculate the midpoints
    data5 = data4 %>%  
      mutate(lower = (bin - 1) * binsize,
             upper = (bin * binsize),
             midpoint = (lower + upper) / 2) %>%
      select(bin,interval, midpoint,  r_obs)
    
    output = data5
    
    # If there are no other rows past the time interval cutoff
    # just output the result
  }else{
    
    output = data1
  }
  
  return(output)
}

