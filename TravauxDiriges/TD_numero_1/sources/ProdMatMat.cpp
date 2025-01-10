#include <algorithm>
#include <cassert>
#include <iostream>
#include <thread>
#if defined(_OPENMP)
#include <omp.h>
#endif
#include "ProdMatMat.hpp"

namespace {
void prodSubBlocks(int iRowBlkA, int iColBlkB, int iColBlkA, int szBlock,
                   const Matrix& A, const Matrix& B, Matrix& C) {
  for (int k = iColBlkA; k < std::min(A.nbCols, iColBlkA + szBlock); k++)
    for (int j = iColBlkB; j < std::min(B.nbCols, iColBlkB + szBlock); j++)
      for (int i = iRowBlkA; i < std::min(A.nbRows, iRowBlkA + szBlock); ++i)
        C(i, j) += A(i, k) * B(k, j);
}
const int szBlock = 128;
}  // namespace

Matrix operator*(const Matrix& A, const Matrix& B) {
  Matrix C(A.nbRows, B.nbCols, 0.0);
# pragma omp parallel for
  for (int J = 0; J < B.nbCols; J += szBlock )
    for (int K = 0; K < A.nbCols; K += szBlock )
      for (int I = 0; I < A.nbRows; I += szBlock )
        prodSubBlocks(I, J, K, szBlock, A, B, C);
  return C;
}
