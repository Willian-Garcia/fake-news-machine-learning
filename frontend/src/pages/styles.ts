import styled from "styled-components";

const primaryColor = "#1a1a1a";
const accentColor = "#d72638";
const backgroundColor = "#f4f4f4";
const cardBackground = "#ffffff";
const borderRadius = "8px";
const shadow = "0 4px 12px rgba(0, 0, 0, 0.05)";
const fontStack = "'Segoe UI', 'Helvetica Neue', sans-serif";

export const Container = styled.div`
  max-width: 800px;
  width: 95%;
  margin: 3rem auto;
  padding: 2rem;
  background-color: ${cardBackground};
  border-radius: ${borderRadius};
  box-shadow: ${shadow};
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

export const Title = styled.h1`
  text-align: center;
  font-size: 2.5rem;
  font-weight: 600;
  color: ${primaryColor};
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-family: ${fontStack};
`;

export const Input = styled.textarea`
  padding: 1rem;
  font-size: 1.1rem;
  border-radius: ${borderRadius};
  border: 1px solid #ccc;
  resize: vertical;
  min-height: 140px;
  background-color: #fff;
  font-family: ${fontStack};

  &:focus {
    border-color: ${accentColor};
    outline: none;
  }
`;

export const Button = styled.button`
  background-color: ${accentColor};
  color: #fff;
  font-size: 1rem;
  padding: 0.9rem 1.2rem;
  border: none;
  border-radius: ${borderRadius};
  cursor: pointer;
  transition: background 0.3s ease;
  font-weight: 500;

  &:hover {
    background-color: #b81e2e;
  }

  &:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
`;

export const ResultBox = styled.div<{ classe?: string }>`
  background-color: ${cardBackground};
  padding: 1rem 1.25rem;
  border-radius: ${borderRadius};
  border-left: 4px solid ${accentColor};
  box-shadow: ${shadow};
  font-family: ${fontStack};
`;

export const Label = styled.p`
  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: ${primaryColor};

  strong {
    color: #000;
  }
`;

export const Loader = styled.div`
  text-align: center;
  font-size: 1rem;
  color: #666;
`;

export const HistoryContainer = styled(Container)`
  margin-top: 4rem;
  gap: 1rem;
`;

export const HistoryTitle = styled.h2`
  text-align: center;
  font-size: 1.8rem;
  color: ${primaryColor};
  font-weight: 500;
  font-family: ${fontStack};
`;
