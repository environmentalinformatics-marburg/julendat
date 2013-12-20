VColList <- list(
  Ta_200 = colorRampPalette(rev(brewer.pal(11, "Spectral"))),
  
  Ta_200_max = colorRampPalette(rev(brewer.pal(11, "Spectral"))),
  
  Ta_200_min = colorRampPalette(rev(brewer.pal(11, "Spectral"))),
  
  Ta_10 = colorRampPalette(rev(brewer.pal(11, "Spectral"))),
  
  Ta_10_max = colorRampPalette(rev(brewer.pal(11, "Spectral"))),
    
  Ta_10_min = colorRampPalette(rev(brewer.pal(11, "Spectral"))),
  
  SM_40 = colorRampPalette(brewer.pal(9, "PuOr")),
  
  SM_20 = colorRampPalette(brewer.pal(9, "PuOr")),
  
  SM_10 = colorRampPalette(brewer.pal(9, "PuOr")),
  
  rH_200 = colorRampPalette(brewer.pal(9, "PuOr")),
  
  Ts_5 = colorRampPalette(rev(brewer.pal(11, "Spectral"))),

  Ts_5_min = colorRampPalette(rev(brewer.pal(11, "Spectral"))),

  Ts_5_max = colorRampPalette(rev(brewer.pal(11, "Spectral"))),
  
  Ts_10 = colorRampPalette(rev(brewer.pal(11, "Spectral"))),

  Ts_10_min = colorRampPalette(rev(brewer.pal(11, "Spectral"))),

  Ts_10_max = colorRampPalette(rev(brewer.pal(11, "Spectral"))),
  
  Ts_20 = colorRampPalette(rev(brewer.pal(11, "Spectral"))),

  Ts_20_min = colorRampPalette(rev(brewer.pal(11, "Spectral"))),

  Ts_20_max = colorRampPalette(rev(brewer.pal(11, "Spectral"))),

  Ts_50 = colorRampPalette(rev(brewer.pal(11, "Spectral"))),

  Ts_50_min = colorRampPalette(rev(brewer.pal(11, "Spectral"))),

  Ts_50_max = colorRampPalette(rev(brewer.pal(11, "Spectral"))),
  
  SWDR_300 = colorRampPalette(rev(brewer.pal(9, "YlGnBu"))),
  
  SWUR_300 = colorRampPalette(rev(brewer.pal(9, "YlGnBu"))),
  
  LWDR_300 = colorRampPalette(rev(brewer.pal(9, "YlGnBu"))),
  
  LWUR_300 = colorRampPalette(rev(brewer.pal(9, "YlGnBu"))),
  
  WD = colorRampPalette(c("red2", "darkblue", "darkgreen", 
                          "gold", "red2"),  interpolate = "linear"),
  
  WV = colorRampPalette(brewer.pal(9, "BuPu")),
  
  p_200 = colorRampPalette(rev(brewer.pal(11, "Spectral"))),
  
  P_RT_NRT = function(n) {
    c("grey10", colorRampPalette(c(rev(brewer.pal(11, "Spectral")), "snow"))(n))
  },

  P_RT_NRT_01 = function(n) {
    c("grey10", colorRampPalette(c(rev(brewer.pal(11, "Spectral")), "snow"))(n))
  },

  P_RT_NRT_02 = function(n) {
    c("grey10", colorRampPalette(c(rev(brewer.pal(11, "Spectral")), "snow"))(n))
  },

  F_RT_NRT_01 = function(n) {
    c("grey10", colorRampPalette(c(rev(brewer.pal(11, "Spectral")), "snow"))(n))
  },

  F_RT_NRT_02 = function(n) {
    c("grey10", colorRampPalette(c(rev(brewer.pal(11, "Spectral")), "snow"))(n))
  },

  F_RT_NRT = function(n) {
    c("grey10", colorRampPalette(c(rev(brewer.pal(11, "Spectral")), "snow"))(n))
  })