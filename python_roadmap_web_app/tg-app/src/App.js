import React from 'react';
import { ChakraProvider, Box, Heading, Text } from '@chakra-ui/react';

function Page() {
  return (
    <ChakraProvider>
      <Box p={5}>
        <Heading as="h1" size="2xl" mb={4}>
          Главный заголовок
        </Heading>
        <Heading as="h2" size="xl" mb={4}>
          Подзаголовок уровня 1
        </Heading>
        <Heading as="h3" size="lg" mb={4}>
          Подзаголовок уровня 2
        </Heading>
        <Text fontSize="md">
          Здесь может быть ваш текст.
        </Text>
      </Box>
    </ChakraProvider>
  );
}

export default Page;
