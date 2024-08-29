import React from 'react';
import { Typography, Box } from '@mui/material';

function Page() {
  return (
    <Box p={3}>
      <Typography variant="h1">Главный заголовок</Typography>
      <Typography variant="h2">Подзаголовок уровня 1</Typography>
      <Typography variant="h3">Подзаголовок уровня 2</Typography>
      <Typography variant="h4">Подзаголовок уровня 3</Typography>
    </Box>
  );
}

export default Page;
