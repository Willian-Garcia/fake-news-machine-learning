import React, { useState } from "react";
import axios from "axios";
import {
  Container,
  Title,
  Input,
  Button,
  ResultBox,
  Label,
  Loader,
  HistoryContainer,
  HistoryTitle,
} from "./styles";

type Resultado = {
  classe: string;
  probabilidade: number;
  palavras_influentes: string[];
};

const FakeNewsScreen: React.FC = () => {
  const [texto, setTexto] = useState("");
  const [resultado, setResultado] = useState<Resultado | null>(null);
  const [historico, setHistorico] = useState<Resultado[]>([]);
  const [loading, setLoading] = useState(false);

  const handleVerificar = async () => {
    setLoading(true);
    setResultado(null);

    try {
      const response = await axios.post<Resultado>(
        "http://localhost:8000/api/classificar-noticia",
        {
          texto,
          usar_exemplo: false,
        }
      );

      setResultado(response.data);
      setHistorico((prev) => [response.data, ...prev]);
    } catch (error) {
      alert("Erro ao classificar notícia.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Title>Classificador de Fake News</Title>
      <Container>
        <Input
          placeholder="Digite uma notícia em inglês..."
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
        />
        <Button
          onClick={handleVerificar}
          disabled={loading || texto.length < 10}
        >
          Verificar
        </Button>

        {loading && <Loader>Carregando...</Loader>}

        {resultado && (
          <ResultBox>
            <Label>
              Classificação: <strong>{resultado.classe.toUpperCase()}</strong>
            </Label>
            <Label>
              Probabilidade:{" "}
              <strong>{(resultado.probabilidade * 100).toFixed(2)}%</strong>
            </Label>
            {resultado.palavras_influentes.length > 0 && (
              <Label>
                Palavras influentes:{" "}
                <strong>{resultado.palavras_influentes.join(", ")}</strong>
              </Label>
            )}
          </ResultBox>
        )}
      </Container>

      {historico.length > 0 && (
        <HistoryContainer>
          <HistoryTitle style={{ fontSize: "1.5rem" }}>Histórico</HistoryTitle>
          {historico.map((item, idx) => (
            <ResultBox key={idx}>
              <Label>
                Classificação: <strong>{item.classe.toUpperCase()}</strong>
              </Label>
              <Label>
                Probabilidade:{" "}
                <strong>{(item.probabilidade * 100).toFixed(2)}%</strong>
              </Label>
              {item.palavras_influentes.length > 0 && (
                <Label>
                  Palavras influentes:{" "}
                  <strong>{item.palavras_influentes.join(", ")}</strong>
                </Label>
              )}
            </ResultBox>
          ))}
        </HistoryContainer>
      )}
    </div>
  );
};

export default FakeNewsScreen;
