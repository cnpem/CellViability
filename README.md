# ILUM - IP3 2024.2 (Proposta 20241479)

Projeto de Introdução a Pesquisa III (2024.2): Implementação de rotinas para processamento de imagens de microscopia ótica

## Introdução e motivação

O Laboratório Nacional de Biociências (LNBio) do Centro Nacional de Pesquisa em Energia e Materiais (CNPEM) requer computação de alto desempenho para processamento e análise de imagens geradas por microscopia. Uma das demandas de processamento computacional é a análise de experimentos de triagem biológica automatizada em alta escala (do inglês, High-Throughput Screening; HTS) para a busca de novos fármacos.

O equipamento Operetta da Perkin Elmer, sob responsabilidade da Facility de Bioensaios, captura imagens para triagem de alvos, vias ou eventos celulares expostos a uma biblioteca de compostos em diferentes concentrações em placa de múltiplos poços. Estas placas são submetidas à radiação eletromagnética com comprimentos de ondas específicos, captando as características da estrutura celular e dos patógenos em cada poço em imagens. Devido à complexidade e volume de dados, a análise manual é extremamente laboriosa, sendo necessárias rotinas (semi-)automatizadas para avaliação das características morfológicas da estrutura celular e dos patógenos.

Atualmente, a infraestrutura de armazenamento e processamento de imagens biológicas está sendo migrada do servidor Columbus da Perkin Elmer para o cluster de computação de alto desempenho (do inglês, High Performance Computing; HPC) Marvin (https://marvin.cnpem.br), hospedado no Data Center do SIRIUS/LNLS. O banco de dados de imagens foi transferido do servidor Columbus para o OMERO (www.openmicroscopy.org/omero/), hospedado no HPC Marvin. No entanto, os protocolos de processamento e análise das imagens biológicas ainda estão limitados aos protocolos do servidor Columbus. 

A partir do OMERO e da capacidade de processamento do HPC Marvin, as tarefas de processamento e análise serão atendidas por protocolos construídos a partir de programas de código livre e aberto, como o Cellprofiler (https://cellprofiler.org/) e o Fiji (https://fiji.sc/), que executam algoritmos de visão computacional e também adotam métodos de aprendizado de máquina para segmentação e classificação de estruturas celulares, como citoesqueleto e núcleo.

## Objetivos

Desenvolver protocolos de processamento de imagens de microscopia ótica de células para experimentos HTS, construídos a partir de programas de código livre e aberto, e aproveitando o poder computacional da infraestrutura do HPC Marvin.
