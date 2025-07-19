import java.util.Random;
import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.util.Collections;

/**
 * 数独（Numberplace）の問題を自動生成し、解答も同時に出力するプログラムです。
 * - 完全な解を持つ盤面をランダムに生成
 * - 空白マスを削除し、一意解になるよう調整
 * - 問題と解答を共に標準出力で表示
 */

public class NumberplaceGenerator {
	
	static final Random rnd = new Random();
	
	/**
	* 指定セル (i,j) に digit を確定させた上で、その影響を行・列・3×3 ブロックに伝播させ、
	* 他のセルの候補（bit 表現）から digit を取り除きます。
	*
	* @param kouhoBits 各セルの候補を bitmask (short) で保持
	* @param i 行インデックス (0–8)
	* @param j 列インデックス (0–8)
	* @param digit 取り除く数字（0–8 で 1–9 に対応）
	*/	
	private static void eliminate(short[][] kouhoBits, int i, int j, int digit) {
		
		short mask = (short) ~(1 << digit);
		
		for (int k = 0; k < 9; k++) {
			
			kouhoBits[i][k] &= mask;
			kouhoBits[k][j] &= mask;
			
		}
		
		int bi = (i / 3) * 3, bj = (j / 3) * 3;
		
		for (int ii = bi; ii < bi + 3; ii++)
			for (int jj = bj; jj < bj + 3; jj++)
				kouhoBits[ii][jj] &= mask;
		
	}
	
	/**
	* 再帰的に探索し、与えられた部分盤面に対して「解が何通りあるか」を、
	* 上限 limit に達した時点で打ち切る形でカウントします。
	*
	* @param sudoku 現在の盤面（0 は未確定セル）
	* @param kouhoBits 候補数字の bitmask
	* @param limit 最大探索数（多解チェック用に 2 などを渡す）
	* @return 見つかった解の個数（ただし limit 以上であれば limit が返る）
	*/
	private static int countSolutionsLimited(int[][] sudoku, short[][] kouhoBits, int limit) {
		
		int min = 10, row = -1, col = -1;
		
		for (int i = 0; i < 9; i++)
			for (int j = 0; j < 9; j++)
				if (sudoku[i][j] == 0) {
					
					int count = Integer.bitCount(kouhoBits[i][j]);
					
					if (count == 0) return 0;
					
					if (count < min) {
						min = count;
						row = i;
						col = j;
					}
					
				}
		
		if (row == -1) return 1;
		
		short mask = kouhoBits[row][col];
		int found = 0;
		
		for (int d = 0; d < 9; d++) {
			
			if ((mask & (1 << d)) != 0) {
				
				int[][] sudokuCopy = copySudoku(sudoku);
				short[][] kouhoCopy = copyKouhoBits(kouhoBits);
				
				sudoku[row][col] = d + 1;
				eliminate(kouhoBits, row, col, d);
				
				int sub = countSolutionsLimited(sudoku, kouhoBits, limit - found);
				
				found += sub;
				
				if (found >= limit) return found;
				
				sudoku = sudokuCopy;
				kouhoBits = kouhoCopy;
				
			}
			
		}
		
		return found;
		
	}
	
	/**
	* 完全解付きの数独盤面（全セルに数字が入った状態）を生成します。
	* 内部的にはランダム配置＋バックトラックによる解法を組み合わせています。
	*
	* @return 生成された 9×9 の完全解盤面
	*/
	private static int[][] generateFullSolvedSudoku() {
		
		int[][] sudoku = new int[9][9];
		
		fillSudoku(sudoku);
		
		return sudoku;
		
	}
	
	/**
	* 再帰的バックトラックで未確定セルにランダムな候補を埋めていき、
	* 数独として正しい完全解を目指すメソッドです。
	*
	* @param sudoku 9×9 の部分盤面（0 は未確定）
	* @return 完全に埋められる場合 true、途中で行き詰まると false
	*/
	private static boolean fillSudoku(int[][] sudoku) {
		
		for (int i = 0; i < 9; i++)
			for (int j = 0; j < 9; j++)
				if (sudoku[i][j] == 0) {
					
					List<Integer> nums = new ArrayList<>();
					
					for (int n = 1; n <= 9; n++) nums.add(n);
					
					Collections.shuffle(nums);
					
					for (int val : nums) {
						
						if (isValid(sudoku, i, j, val)) {
							
							sudoku[i][j] = val;
							if (fillSudoku(sudoku)) return true;
							sudoku[i][j] = 0;
							
						}
					}
					
					return false;
					
				}
		
		return true;
		
	}
	
	/**
	* 値 val を (row, col) に配置して矛盾がないかチェックします。
	* 同じ行・列・3×3 ブロック内に val が存在しないかを確認。
	*
	* @return 矛盾なければ true、あれば false
	*/
	private static boolean isValid(int[][] board, int row, int col, int val) {
		
		for (int k = 0; k < 9; k++)
		
		if (board[row][k] == val || board[k][col] == val)
			return false;
		
		int bi = (row / 3) * 3, bj = (col / 3) * 3;
		
		for (int i = bi; i < bi + 3; i++)
			for (int j = bj; j < bj + 3; j++)
				if (board[i][j] == val)
					return false;
		
		return true;
		
	}
	
	private static int[][] copySudoku(int[][] src) {
		
		int[][] dst = new int[9][9];
		
		for (int i = 0; i < 9; i++)
			for (int j = 0; j < 9; j++)
				dst[i][j] = src[i][j];
		
		return dst;
		
    }
	
	private static short[][] copyKouhoBits(short[][] src) {
		
		short[][] dst = new short[9][9];
		
		for (int i = 0; i < 9; i++)
			for (int j = 0; j < 9; j++)
				dst[i][j] = src[i][j];
		
		return dst;
		
	}
	
	/**
	* 解付き盤面から blanks 個のマスを穴あけし、「解が一意になる」ように調整します。
	* ランダムにセルを選び、その度に解のユニーク性を確保できるかチェックします。
	*
	* @param solution 完全解付き盤面
	* @param blanks 空白マスの数
	* @return 空白マスが設定された数独問題（解は solution）
	*/
	private static int[][] generateUniqueProblemFromSolution(int[][] solution, int blanks) {
		
		int[][] puzzle = copySudoku(solution);
		
		List<int[]> cells = new ArrayList<>();
		
		for (int i = 0; i < 9; i++)
			for (int j = 0; j < 9; j++)
				cells.add(new int[]{i, j});
		
		Collections.shuffle(cells);
		
		int removed = 0;
		
		for (int[] cell : cells) {
			
			if (removed >= blanks) break;
			
			int i = cell[0], j = cell[1];
			int backup = puzzle[i][j];
			
			puzzle[i][j] = 0;
			
			short[][] kouhoBits = new short[9][9];
			
			for (int x = 0; x < 9; x++)
				for (int y = 0; y < 9; y++)
				kouhoBits[x][y] = (short) 0b111111111;
			
			for (int x = 0; x < 9; x++)
				for (int y = 0; y < 9; y++)
					if (puzzle[x][y] > 0)
						eliminate(kouhoBits, x, y, puzzle[x][y] - 1);
			
			if (countSolutionsLimited(copySudoku(puzzle), kouhoBits, 2) == 1) {
				
				removed++;
				
			} else {
				
				puzzle[i][j] = backup;
				
			}
			
		}
		
		return puzzle;
		
	}
	
	/**
	* 盤面を文字列として StringBuilder に出力します。
	* デバッグや結果表示用です。
	*
	* @param board 表示対象の盤面
	* @param sb 出力先 StringBuilder
	*/
	private static void printBoard(int[][] board, StringBuilder sb) {
		
		for (int i = 0; i < 9; i++)
			sb.append(Arrays.toString(board[i])).append("\n");
		
	}
	
	
	public static void main(String[] args) {
		
		int blanks = 50;  // 作成する問題の空白マス数を指定
		
		// 完全解盤面の生成
		int[][] solved = generateFullSolvedSudoku();
		
		// ユニーク解な問題盤面を生成
		int[][] problem = generateUniqueProblemFromSolution(solved, blanks);
		
		// 問題と解答を標準出力
		
		StringBuilder sb = new StringBuilder(520);
		
		sb.append("\u25A0 問題:\n");
		printBoard(problem, sb);
		
		sb.append("\n\u25A0 解答:\n");
		printBoard(solved, sb);
		
		System.out.println(sb.toString().trim());
		
	}
	
}