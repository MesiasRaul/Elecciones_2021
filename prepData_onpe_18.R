# Objetivo: Preparar la data descargada mediante web scraping #

library(readxl)
library(dplyr)
library(ggplot2)
library(stringr)

setwd(dir = "C:/Users/ASUS/Desktop/PC/9.Proyectos/1.analitica_elecciones_2021")

data = read_xlsx(path = "1.insumos/resultado_2018_distrito.xlsx")
data = data[,2:6]

data = data %>% rename(DETALLE_VOTO = B,
                       NIVEL_PROVINCIAL = C,
                       NIVEL_DISTRITAL = D,
                       NUMERO_MESA = columna_name)

data = data %>% mutate(NIVEL_DISTRITAL = ifelse(test = !is.na(A),yes = as.numeric(NIVEL_PROVINCIAL),no = as.numeric(NIVEL_DISTRITAL)),
                       NIVEL_PROVINCIAL = ifelse(test = !is.na(A),yes = as.numeric(DETALLE_VOTO),no = as.numeric(NIVEL_PROVINCIAL)),
                       DETALLE_VOTO = ifelse(test = !is.na(A),yes = A,no = DETALLE_VOTO)) %>%
  group_by(DETALLE_VOTO) %>%
  summarise(NIVEL_PROVINCIAL = sum(NIVEL_PROVINCIAL,na.rm = T),
            NIVEL_DISTRITAL = sum(NIVEL_DISTRITAL,na.rm = T)) %>%
  mutate(OP_DET = ifelse(test = !grepl(pattern = "^TOTAL|^VOTO",x = DETALLE_VOTO),yes = "OP",no = "DET")) %>%
  arrange(OP_DET,desc(NIVEL_DISTRITAL)) %>%
  mutate(DETALLE_VOTO = as.factor(DETALLE_VOTO),
         OP_DET = as.factor(OP_DET)) %>%
  filter(!grepl(pattern = "TOTAL VOTOS",x = DETALLE_VOTO))

data = data %>% mutate(DETALLE_VOTO_2 =  str_wrap(string = DETALLE_VOTO,width = 10))


# data$OP_DET = NULL
# rm(data)

# Gráficos ####
sapply(data,class)
ggplot(data,aes(x = reorder(DETALLE_VOTO_2,NIVEL_DISTRITAL),y = NIVEL_DISTRITAL,fill = OP_DET)) +
  geom_bar(stat = "identity",colour = "black") +
  scale_x_discrete(guide = guide_axis(n.dodge = 1)) +
  scale_fill_manual(values=c("#669933", "#FFCC66")) +
  geom_text(aes(label = NIVEL_DISTRITAL), vjust = -0.7) +
  ggtitle(label = "Elecciones 2018 - Ciudad de Carhuamayo") +
  theme(plot.title = element_text(hjust = 0.5)) +
  ylab(label = "Votos") +
  xlab(label = NULL) +
  guides(fill=FALSE)
